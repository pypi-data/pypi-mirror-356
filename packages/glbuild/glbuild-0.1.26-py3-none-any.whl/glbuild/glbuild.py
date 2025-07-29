"""Main Class for GitLab Builds data collection"""

import math
import time
import json
import gitlab
import logging
import requests
from tqdm import tqdm, trange
from typing import Any, Optional

from glbuild import constants
from glbuild.storage.abstract_storage import AbstractStorage
from glbuild.storage.local_storage import LocalStorage
from requests.exceptions import ChunkedEncodingError
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)  # type: ignore


logging.basicConfig(level=logging.INFO)


class GitLabBuild:
    """GitLabBuild Class."""

    def __init__(
        self,
        token: str,
        projects: list[int],
        base_url: str = constants.GITLAB_BASE_URL,
        api_version: int = 4,
        ssl_verify: bool = False,
        output: str = constants.LOCAL_DATA_BASE_DIR,
        storage: Optional[AbstractStorage] = None,
        only_failure_logs: bool = True,
    ) -> None:
        """Constructor.

        Params
        ------
            projects (list[int]|int): Single of List of projects ID.
            base_url (str): GitLab instance base URL. Defaults to https://gitlab.com
            token (str): GitLab Personal Access Token.
            output (str | None): Data directory path for LocalStorage. Defaults to `./data/`. Ignored if a custom storage is specified.
            storage (AbstractStorage | None): Storage implementation. If `None`, Defaults to new `LocalStorage()` with `output` as base directory.
        """
        self.logger = logging.getLogger(__name__)
        self.base_url: str = base_url
        self.token: str = token
        self.api_version: int = api_version
        self.ssl_verify: bool = ssl_verify
        self.projects = projects
        self.gl = gitlab.Gitlab(
            url=base_url,
            private_token=token,
            api_version=api_version,
            ssl_verify=ssl_verify,
        )
        self.storage = storage or LocalStorage(base_dir=output, projects=projects)
        self.only_failure_logs = only_failure_logs

    def start(
        self,
        n_last: Optional[int] = None,
        refresh: bool = True,
        historical: bool = False,
    ) -> bool:
        """Get historical build jobs metadata and logs from projects into path.

        As a default, historical data is collected if there is no existing data, and updated otherwise if refresh is set to `True`.

        Params
        ------
            n_last (int | None): Get only n last jobs. If `None`, attempts to collect all data. Defaults to `None`.
            refresh (bool): Whether to refresh data by collecting only newly available data. Defaults to `True`.
            historical (bool): If `True`, continue `n_last` historical data collection (generally after an error). Defaults to `False`.

        Returns
        -------
            (bool): Whether data collection was successfully completed or not.
        """
        try:
            self.gl.auth()
        except gitlab.exceptions.GitlabAuthenticationError as error:
            self.logger.error("Authentication to GitLab failed: %s", error)
            return False

        self.storage.ensure_storage_available()

        for project_id in self.projects:
            self.__collect_project_data(
                project_id, n_last=n_last, refresh=refresh, historical=historical
            )
            time.sleep(1)

        self.logger.info("Data collection completed sucessfully :)")
        return True

    ###################################
    #         Project Methods         #
    ###################################

    def __collect_project_data(
        self,
        project_id: int,
        n_last: Optional[int] = None,
        refresh: bool = True,
        historical: bool = False,
    ):
        """Collect and save jobs metadata and logs for a GitLab project.

        project_id (int): ID of the project.
        n_last (None|int): Get only n last jobs.
        refresh (bool): Whether to refresh data by collecting only newly available data. Defaults to `True`.
        historical (bool): If `True`, continue `n_last` historical data collection (generally after an error). Defaults to `False`.
        """
        self.logger.info("Starting data collection for project %s...", project_id)

        old_count, last_id = self.storage.count_and_last_id(project_id)

        if old_count == 0 or historical:
            if old_count == 0:
                self.logger.info("No existing data found")
            self.__collect_job_history(project_id, n_last, offset=old_count)
        elif refresh:
            self.logger.info(
                "%s already collected jobs. Refreshing...", old_count
            )  # noqa
            count_new = 0
            for c in tqdm(self.__refresh_job_history(project_id, last_id), ncols=120):
                count_new += c
            self.logger.info("%s additionnal jobs collected", count_new)
        else:
            pass

    ###################################
    #           Job Methods           #
    ###################################

    def __refresh_job_history(self, project_id, last_id: int):
        """Collect new data up to `last_id`."""
        page: int = 0
        latest_jobs: list[dict] = []
        while last_id not in [j["id"] for j in latest_jobs]:
            page = page + 1
            count, next_jobs = self.__collect_jobs_and_logs(project_id, page=page)
            latest_jobs.extend(next_jobs)
            yield count

    def __collect_job_history(self, project_id, n_last: Optional[int], offset: int):
        """Get list of all jobs for a project using python-gitlab limited to `n_last`."""
        # TODO: For LocalStorage JSON always use max last at 25000
        if n_last is None:
            self.logger.info("Collecting entire job history...")
            self.__collect_jobs_and_logs(project_id, all=True)
            return

        per_page = constants.JOBS_PER_PAGE
        if n_last < constants.JOBS_PER_PAGE:
            per_page = n_last

        total_pages = math.ceil(n_last / per_page) + 1
        start_page = math.ceil(offset / per_page) + 1
        self.logger.info(
            "Collecting %s jobs over %s pages",
            n_last - offset,
            total_pages - start_page,
        )

        progress_bar = trange(start_page, total_pages, ncols=120)
        for page in progress_bar:
            try:
                self.__collect_jobs_and_logs(
                    project_id=project_id, page=page, per_page=per_page
                )
            except requests.exceptions.ReadTimeout:
                self.logger.warning("Read timed out. Possible end of read.")
                break
        progress_bar.close()

    def __collect_jobs_and_logs(
        self,
        project_id: int,
        page: int = 1,
        per_page: int = constants.JOBS_PER_PAGE,
        all: bool = False,
    ) -> tuple[int, list[dict]]:
        """Collect and save jobs and logs on a given page for a project using python-gitlab.

        Returns count of new jobs saved and list of jobs collected.
        """
        project = self.gl.projects.get(int(project_id), lazy=True)
        params: dict[str, Any] = {
            "retry_transient_errors": True,
            "timeout": constants.HTTP_REQUESTS_TIMEOUT,
        }
        if all is True:
            params["all"] = True
        else:
            params["page"] = page
            params["per_page"] = per_page

        jobs = [json.loads(job.to_json()) for job in project.jobs.list(**params)]
        count = self.storage.save_jobs(project_id, jobs)
        self.__collect_extra_data(project_id, jobs)
        return count, jobs

    def __collect_extra_data(self, project_id: int, jobs: list[dict]):
        """Collect and save job logs and store pipeline YAML once per pipeline run."""

        # Group jobs by pipeline ID
        pipeline_jobs = {}
        for job in jobs:
            pipeline_id = job["pipeline"]["id"]
            if pipeline_id not in pipeline_jobs:
                pipeline_jobs[pipeline_id] = []
            pipeline_jobs[pipeline_id].append(job)

        for pipeline_id, job_list in pipeline_jobs.items():
            # Identify the first job in the pipeline (to get commit SHA)
            first_job = min(job_list, key=lambda j: j["created_at"])
            commit_sha = first_job["commit"]["id"]

            self.logger.info(
                "Fetching pipeline YAML for pipeline %s in project %s.",
                pipeline_id,
                project_id,
            )

            # Fetch and store the pipeline YAML **only once per pipeline**
            yaml_content = self.__fetch_pipeline_yaml(project_id, commit_sha)
            if yaml_content:
                self.storage.save_pipeline_yaml(project_id, pipeline_id, yaml_content)

            # Collect and store logs for all jobs in the pipeline
            for job in job_list:
                job_id = job["id"]
                if self.only_failure_logs and job["status"] != "failed":
                    continue
                if self.storage.logs_exists(project_id, job_id):
                    continue

                logs = self.__retrieve_job_logs(project_id, job_id)
                if logs is not None:
                    self.storage.save_logs(project_id, job_id, logs)

        self.logger.info(
            "Logs and pipeline YAML files successfully stored for project %s.",
            project_id,
        )
    def __fetch_pipeline_yaml(self, project_id: int, commit_sha: str) -> Optional[str]:
        """
        Fetch the pipeline YAML (.gitlab-ci.yml) used in a specific pipeline run.
        Returns:
           The raw YAML content, or None if retrieval fails.
        """
        url = f"{self.base_url}/api/v4/projects/{project_id}/repository/files/.gitlab-ci.yml/raw?ref={commit_sha}"

        headers = {
            "PRIVATE-TOKEN": self.token,
        }

        try:
            response = requests.get(
                url, headers=headers, timeout=constants.HTTP_REQUESTS_TIMEOUT
            )
            response.raise_for_status()
            return response.text

        except requests.exceptions.HTTPError as http_err:
            self.logger.error(
                f"HTTP error fetching YAML for project {project_id}: {http_err}"
            )
            self.logger.error(f"Request failed for project {project_id}: {err}")

        return None

    def __retrieve_job_logs(
        self, project_id: str | int, job_id: str | int
    ) -> Optional[str]:
        """Get job textual log data from API.

        Returns
        -------
            (str | None): Log data textual content. None if no logs available (e.g., for canceled jobs).
        """
        headers = {
            "PRIVATE-TOKEN": self.token,
        }
        url = f"{self.base_url}/api/v4/projects/{project_id}/jobs/{job_id}/trace"
        try:
            response = requests.get(
                url,
                headers=headers,
                verify=self.ssl_verify,
                timeout=constants.HTTP_REQUESTS_TIMEOUT,
            )
            return response.text
        except ChunkedEncodingError:
            # Empty log
            return None
