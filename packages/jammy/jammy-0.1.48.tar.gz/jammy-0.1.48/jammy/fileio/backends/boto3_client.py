# pylint: disable=too-many-arguments, import-outside-toplevel, import-error
import io
import json
import os

from jammy.logging import get_logger
from jammy.storage.kv.memcached import MemcachedKVStore

logger = get_logger()


class Boto3Client:
    def __init__(
        self,
        conf_path: str,
        max_attempt: int = 3,
        enable_mc=False,
        mc_addr=None,
        mc_port=None,
    ):
        self.max_attempt = max_attempt
        try:
            import boto3
        except ImportError:
            raise ImportError("Please install boto3 to use Boto3Client.")

        with open(conf_path, "r") as f:
            conf = json.load(f)
        self._client = boto3.client("s3", **conf)
        if enable_mc:
            try:
                import memcache
            except ImportError:
                raise ImportError(
                    "Please install python-memcached to use Boto3Client with memcached."
                )
            self._mc_kv_store = MemcachedKVStore(mc_addr, mc_port)
        else:
            self._mc_kv_store = None

    def get(self, filepath):
        filepath = self._check_path(filepath)

        if self._mc_kv_store and self._mc_kv_store.available:
            if self._mc_kv_store.has(filepath):
                return self._mc_kv_store.get(filepath)

        attempt = 0
        while attempt < self.max_attempt:
            try:
                buffer = io.BytesIO()
                self._client.download_fileobj(
                    Bucket=filepath.split("/")[0],
                    Key="/".join(filepath.split("/")[1:]),
                    Fileobj=buffer,
                )
                buffer.seek(0)
                if self._mc_kv_store and self._mc_kv_store.available:
                    self._mc_kv_store.put(filepath, buffer.read())

                return buffer.read()
            except Exception as e:
                attempt += 1
                logger.info(f"Got an exception: attempt={attempt} - {e} - {filepath}")

        raise ConnectionError(
            "Unable to read {} from. {} attempts tried.".format(filepath, attempt)
        )

    def put(self, obj, filepath):
        filepath = self._check_path(filepath)
        bucket_name = filepath.split("/")[0]
        key = "/".join(filepath.split("/")[1:])
        from botocore.exceptions import ClientError

        attempt = 0
        while attempt < self.max_attempt:
            try:
                # If obj is a string path to a local file, use upload_file instead
                if isinstance(obj, str) and os.path.isfile(obj):
                    self._client.upload_file(Filename=obj, Bucket=bucket_name, Key=key)
                    return
                if isinstance(obj, io.BytesIO):
                    obj.seek(0)
                    self._client.upload_fileobj(obj, Bucket=bucket_name, Key=key)
                    return
                if isinstance(obj, bytes):
                    self._client.put_object(Body=obj, Bucket=bucket_name, Key=key)
                    return
                else:
                    raise ValueError("Unsupported object type for upload")
            except ClientError as e:
                attempt += 1
                logger.info(f"Got an exception: attempt={attempt} - {e} - {filepath}")

        raise ConnectionError(
            "Unable to write {} to. {} attempts tried.".format(filepath, attempt)
        )

    def contains(self, filepath: str):
        filepath = self._check_path(filepath)
        from botocore.exceptions import ClientError

        try:
            self._client.head_object(
                Bucket=filepath.split("/")[0], Key="/".join(filepath.split("/")[1:])
            )
            return True
        except ClientError:
            return False

    def isdir(self, filepath: str):
        if self.contains(filepath):
            filepath = self._check_path(filepath)
            if not filepath.endswith("/"):
                filepath += "/"
            resp = self._client.list_objects_v2(
                Bucket=filepath.split("/")[0],
                Prefix="/".join(filepath.split("/")[1:]),
                Delimiter="/",
                MaxKeys=1,
            )
            return "Contents" in resp
        return False

    def delete(self, filepath):
        filepath = self._check_path(filepath)
        self._client.delete_object(
            Bucket=filepath.split("/")[0], Key="/".join(filepath.split("/")[1:])
        )

    def list(self, filepath):
        filepath = self._check_path(filepath)
        resp = self._client.list_objects_v2(
            Bucket=filepath.split("/")[0], Prefix="/".join(filepath.split("/")[1:])
        )
        return [f["Key"] for f in resp["Contents"]]

    def _check_path(self, filepath: str):
        assert filepath.startswith("s3://")
        filepath = filepath[5:]
        return filepath
