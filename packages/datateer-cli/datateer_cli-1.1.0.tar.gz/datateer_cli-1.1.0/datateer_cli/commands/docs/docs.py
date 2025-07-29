import os
import shutil
import subprocess
import sys
import traceback
from time import time

import boto3
import yaml

import datateer_cli.logging as log


def generate_erd(searchdir: str) -> None:
    """
    Generates entity relationship diagrams for upload to the client's site

    Parameters
    ----------
    searchdir: str
        The directory to search for dbt model configuration files. Will recursively search this directory.
    """
    from datateer_cli.commands.docs.generate_erd import generate, SEARCHDIR_DEFAULT
    if searchdir is None:
        searchdir = SEARCHDIR_DEFAULT

    generate(searchdir)


def run_dbt_docs_command(target=None) -> None:
    """
    Runs the dbt docs generate command to create the html that will be uploaded to the client's site.
    """

    command = "dbt docs generate".split()
    if target is not None:
        command = f"dbt docs generate --target {target}".split()
    try:
        process = subprocess.Popen(
            command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        print(stdout, stderr)
        return command
    except Exception:
        print(sys.exc_info())
        raise


def run_aws_s3_sync_command(client_code: str) -> None:
    """
    Uploads newly created documentation to the client's S3 bucket and removes older files.

    Parameters
    ----------
    client_code: str
        The three-character client code.
    """
    command = f"aws s3 cp target/ s3://dbt-docs-666090538019/{client_code} --recursive".split()
    print(f'running command: {command}')
    try:
        process = subprocess.Popen(
            command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        print(stdout, stderr)
        return command
    except Exception:
        print(sys.exc_info())
        raise

    # remove files that don't need to be uploaded to the docs site
    compiled_path = 'target/compiled'
    if os.path.exists(compiled_path):
        print(f"Removing unnecessary files from {compiled_path}")
        shutil.rmtree(compiled_path)


def invalidate_cloudfront_cache() -> None:
    """
    Invalidates the cloudfront cache.

    """
    name = "docs_site_cloudfront_distribution_id"
    client = boto3.client("ssm")
    res = client.get_parameter(Name=name)["Parameter"]["Value"]
    client = boto3.client("cloudfront")
    client.create_invalidation(
        DistributionId=res,
        InvalidationBatch={
            "Paths": {
                "Quantity": 1,
                "Items": ["/*"],
            },
            "CallerReference": str(time()).replace(".", ""),
        },
    )


def deploy_docs(searchdir: str, client_code: str, target: str = None) -> None:
    """
    Generates documentation and deploys it to the client's documentation site.

    Parameters
    ----------
    searchdir: str
        The directory to search for dbt model configuration files. Will recursively search this directory.
    client_code: str
        The three-character client code.
    target: str
        The dbt target environment. Optional.
    """

    generate_erd(searchdir)
    run_dbt_docs_command(target)
    run_aws_s3_sync_command(client_code)
