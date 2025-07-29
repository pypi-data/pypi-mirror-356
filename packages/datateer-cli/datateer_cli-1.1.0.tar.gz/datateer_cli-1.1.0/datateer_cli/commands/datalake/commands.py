from datetime import date
from itertools import islice

import boto3
import click


@click.group(help="Operations on the Datateer Data Lake")
def datalake():
    pass


@datalake.command(help="Remove files created before the specified date")
@click.option(
    "--bucket",
    "-b",
    required=True,
    help="The name of the bucket to remove the objects from",
)
@click.option(
    "--date",
    "-d",
    required=True,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Objects created before this date will be deleted",
)
@click.option(
    "--prefix",
    "-p",
    required=False,
    help="Optional. Will limit the object removal to only objects that have this key prefix",
)
@click.option("--dry-run/--no-dry-run", default=True)
@click.option(
    "--prompt/--no-prompt",
    default=True,
    help="Optional. Will answer prompts yes automatically",
)
def delete_before_date(bucket: str, date: date, prefix: str = "", dry_run: bool = True, prompt: bool = False):
    """Deletes files from bucket before date

    Parameters
    ----------
    bucket: str
        The name of the bucket to remove the objects from
    date: date
        Objects created before this date will be deleted
    prefix: str
        Optional. Will limit the object removal to only objects that have this key prefix
    """
    session = boto3.session.Session()
    bucket_name = bucket
    bucket = session.resource("s3").Bucket(bucket_name)

    objects_to_delete = []
    for obj in bucket.objects.all():
        if (obj.last_modified).replace(tzinfo=None) < date and obj.key.startswith(
            prefix
        ):
            objects_to_delete.append(obj.key)
            if dry_run:
                print(f"Dry run: would delete {obj.key}")
            else:
                print(f"Preparing to delete object {obj.key}")
    if dry_run:
        print(f"Dry run: would have deleted these {len(objects_to_delete)} objects")
    elif prompt:  # User will be prompted to continue with delete
        click.confirm(
            f"Are you SURE you want to delete these {len(objects_to_delete)}?",
            abort=True,
        )
        delete_objects(objects_to_delete, bucket)
    else:  # prompt = false --no-prompt has been chosen User has chosen to delete files without confirmation
        delete_objects(objects_to_delete, bucket)


def delete_objects(objects_to_delete, bucket):
    maximum_to_delete_in_batch = 1000  # AWS API can only delete 1,000 at a time
    while 0 < len(objects_to_delete):
        # filter to an acceptable batch size
        filtered = (o for o in objects_to_delete)
        slice_to_delete = list(islice(filtered, maximum_to_delete_in_batch))

        # do the delete
        bucket.delete_objects(
            Delete={"Objects": [{"Key": k} for k in slice_to_delete]}
        )

        # remove the deleted items
        objects_to_delete = [
            o for o in objects_to_delete if o not in slice_to_delete
        ]
        print(
            f"Deleted {len(slice_to_delete)} objects. {len(objects_to_delete)} remaining"
        )
