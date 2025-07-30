from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import boto3


@dataclass
class AWSAssetStore:
    """Wrapper around boto3 S3 client for basic asset operations."""

    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    region_name: str | None = None

    @classmethod
    def from_env(cls) -> "AWSAssetStore":
        return cls(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )

    def _client(self):
        return boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )

    def upload_file(self, file_path: Path, bucket: str, key: str) -> None:
        """Upload *file_path* to ``s3://bucket/key``."""
        client = self._client()
        client.upload_file(str(file_path), bucket, key)
        print(f"uploaded → s3://{bucket}/{key}")