import click

from .docs import deploy_docs


@click.group(help="Commands related to documentation")
def docs():
    pass


@docs.command(
    help="Deploys docs including erd-diagrams and dbt docs, intended to be used at the root of a pipeline repository"
)
@click.option(
    "-m",
    "--dbt-models-dir",
    default="dbt/models",
    help="The dbt models directory",
    show_default=True,
)
@click.option(
    "-c",
    "--client-code",
    envvar="CLIENT_CODE",
    required=True,
    help="(defaults to env var CLIENT_CODE)",
)
@click.option(
    "-t",
    "--target",
    help="The dbt target environment. Optional"
)
def deploy(client_code, dbt_models_dir, target):
    deploy_docs(dbt_models_dir, client_code, target)
