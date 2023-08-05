from __future__ import annotations
import logging
import boto3
from botocore.response import StreamingBody
from botocore.exceptions import ClientError
from uuid import UUID
import base64
import json
from io import StringIO
import pandas as pd
from typing import BinaryIO

from app.core.config import settings


# https://tenacity.readthedocs.io/en/latest/
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed  # noqa: F401

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 10 * 1  # 10 seconds
wait_seconds = 1
return_value_on_error = {}


class CRUDSpaces:
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD) DigitalOcean Spaces.

        # https://docs.digitalocean.com/products/spaces/resources/s3-sdk-examples/
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#object
        """
        self.space = boto3.resource(
            "s3",
            region_name=settings.SPACES_REGION_NAME,
            endpoint_url=settings.SPACES_ENDPOINT_URL,
            aws_access_key_id=settings.SPACES_ACCESS_KEY,
            aws_secret_access_key=settings.SPACES_SECRET_KEY,
        )
        self.bucket = self.space.Bucket(settings.SPACES_BUCKET)

    def exists(self, *, folder_id: UUID | str | None = None, filename: str) -> bool:
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        obj = self.bucket.Object(key)
        try:
            obj.load()
            return True
        except ClientError:
            return False

    @retry(
        stop=stop_after_attempt(max_tries),
        wait=wait_fixed(wait_seconds),
        after=after_log(logger, logging.WARN),
        retry_error_callback=lambda retry_state: return_value_on_error,
    )
    def get(self, *, folder_id: UUID | str | None = None, filename: str) -> BinaryIO:
        # https://stackoverflow.com/a/35376156/295606
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        obj = self.bucket.Object(key)
        source = obj.get()["Body"].read().decode("utf-8")
        # Convert base64 to binary
        # return base64.b64decode(source)
        # source = base64.b64decode(source)
        # Try this:
        # return json.loads(source.decode("utf8"))
        return json.loads(source)

    def fix_source(self, *, folder_id: UUID | str | None = None, filename: str) -> BinaryIO:
        # https://stackoverflow.com/a/35376156/295606
        # For copying json hexbins ... plus updates
        # Probably happens if you copy a 'raw' json file into spaces
        # https://github.com/odileeds/hexmaps/tree/gh-pages/maps
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        obj = self.bucket.Object(key)
        source = obj.get()["Body"].read().decode("utf-8")
        obj_in = json.loads(source)
        save_obj = base64.b64encode(json.dumps(obj_in).encode())
        self.update(folder_id=folder_id, filename=filename, source=save_obj)

    def get_stream(self, *, folder_id: UUID | str | None = None, filename: str) -> StreamingBody:
        # https://stackoverflow.com/questions/69617252/response-file-stream-from-s3-fastapi
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        try:
            obj = self.bucket.Object(key)
            return obj.get()["Body"].iter_chunks()
        except Exception as e:
            print("-----------------------------------------------------------")
            print(f"ERROR: Spaces Stream     -     {filename}")
            print("-----------------------------------------------------------")
            raise e

    def save_stream(self, *, folder_id: UUID | str | None = None, filename: str, df: pd.DataFrame) -> None:
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        try:
            obj = self.bucket.Object(key)
            source = StringIO()
            df.to_csv(source, index=False)
            source.seek(0)
            obj.put(Body=source.getvalue())
        except Exception as e:
            print("-----------------------------------------------------------")
            print(f"Spaces Save     -     {filename}")
            print("-----------------------------------------------------------")
            raise e

    def upload_file(self, *, folder_id: UUID | str | None = None, filename: str, source_path: str) -> None:
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        self.bucket.upload_file(Filename=source_path, Key=key)

    def download_file(self, *, folder_id: UUID | str | None = None, filename: str, source_path: str) -> None:
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        self.bucket.download_file(Filename=source_path, Key=key)

    def create(self, *, folder_id: UUID | str | None = None, filename: str, source: str) -> int:
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        obj = self.bucket.Object(key)
        obj.put(Body=source)

    @retry(
        stop=stop_after_attempt(max_tries),
        wait=wait_fixed(wait_seconds),
        after=after_log(logger, logging.WARN),
    )
    def update(self, *, folder_id: UUID | str | None = None, filename: str, source: str) -> int:
        try:
            self.create(folder_id=folder_id, filename=filename, source=source)
        except Exception as e:
            logger.error(e)
            raise e

    def rename(self, *, folder_id: UUID | str | None = None, oldname: str, newname: str) -> None:
        old_key = f"{oldname}"
        if folder_id:
            old_key = f"{folder_id}/{oldname}"
        old_obj = {"Bucket": settings.SPACES_BUCKET, "Key": old_key}
        new_key = f"{newname}"
        if folder_id:
            new_key = f"{folder_id}/{newname}"
        self.bucket.copy(old_obj, new_key)
        self.bucket.Object(old_key).delete()

    def remove(self, *, folder_id: UUID | str | None = None, filename: str) -> int:
        key = f"{filename}"
        if folder_id:
            key = f"{folder_id}/{filename}"
        obj = self.bucket.Object(key)
        obj.delete()


spaces = CRUDSpaces()
