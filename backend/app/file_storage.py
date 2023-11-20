"""Module for storing files using s3 compatible storage."""
# mypy: ignore-errors
import os
import tempfile
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3
from botocore.config import Config
from minio import Minio


@dataclass
class FileStorage:
    """Class for storing files using s3 compatible storage."""

    client: Optional[boto3.client] = None
    bucket_name: str = os.environ["S3_BUCKET"]

    def upload_source(
        self, file: bytes, id: str, source_type: str, bot_id: str
    ) -> None:
        """Upload a source file to the storage."""
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=f"sources/{bot_id}/{id}.{source_type}",
            Body=file,
        )

    def download_source(self, id: str, source_type: str, bot_id: str) -> str:
        """Get a source file from the storage."""
        # fd, path = tempfile.mkstemp(suffix=f".{source_type}")
        # with os.fdopen(fd, "wb") as tmp:
        #     self.client.download_fileobj(
        #         self.bucket_name, f"sources/{bot_id}/{id}.{source_type}", tmp
        #     )
        # return path
        response = self.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": f"sources/{bot_id}/{id}.{source_type}",
            },
            ExpiresIn=3600,
        )
        return response

    def delete_source(self, id: str, source_type: str, bot_id: str) -> None:
        """Delete a source file from the storage."""
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=f"sources/{bot_id}/{id}.{source_type}",
        )


@lru_cache()
def get_s3_client() -> boto3.client:
    """Get the database."""
    client = boto3.client(
        service_name="s3",
        endpoint_url=os.environ["S3_ENDPOINT"],
        aws_access_key_id=os.environ["S3_ACCESS_KEY"],
        aws_secret_access_key=os.environ["S3_SECRET_KEY"],
        config=Config(signature_version="s3v4"),
    )
    return client
