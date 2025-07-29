"""Main CLI tool module."""

import click
from glbuild import GitLabBuild


@click.group(invoke_without_command=True)
@click.option("--token", "-t", type=str, required=True)
@click.option("--project", "-p", required=True, multiple=True)
@click.option("--n-last", "-n", type=int, required=False, help="Get n last jobs only")
@click.option("--output", "-o", type=str, default="./data", help="Output directory")
@click.option("--base-url", "-b", type=str, default="https://gitlab.com")
@click.option("--api-version", type=int, default=4)
@click.option("--ssl-verify", type=bool, default=False)
@click.option("--only-failure-logs", type=bool, default=True)
@click.option("--historical", "-h", type=bool, default=False)
@click.option("--refresh", "-r", type=bool, default=True)
def cli(
    token,
    project,
    n_last,
    output,
    base_url,
    api_version,
    ssl_verify,
    only_failure_logs,
    historical,
    refresh,
):
    """Glbuild CLI.

    Collect historical GitLab build data easily.
    """
    glb = GitLabBuild(
        base_url=base_url,
        token=token,
        projects=list(project),
        api_version=api_version,
        ssl_verify=ssl_verify,
        output=output,
        only_failure_logs=only_failure_logs,
    )
    glb.start(n_last=n_last, refresh=refresh, historical=historical)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    cli()
