"""Rucio plugin for Snakemake."""

from __future__ import annotations

import dataclasses
import inspect
import random
import re
from collections.abc import Iterable, Sequence
from urllib.parse import urlparse

import rucio.client
import rucio.client.baseclient
import rucio.client.downloadclient
import rucio.client.uploadclient
import rucio.common.exception
from snakemake_interface_common.logging import get_logger
from snakemake_interface_storage_plugins.io import IOCacheStorageInterface, Mtime
from snakemake_interface_storage_plugins.settings import StorageProviderSettingsBase
from snakemake_interface_storage_plugins.storage_object import (
    StorageObjectGlob,
    StorageObjectRead,
    StorageObjectWrite,
    retry_decorator,
)
from snakemake_interface_storage_plugins.storage_provider import (
    ExampleQuery,
    Operation,
    QueryType,
    StorageProviderBase,
    StorageQueryValidationResult,
)

# Optional:
# Define settings for your storage plugin (e.g. host url, credentials).
# They will occur in the Snakemake CLI as --storage-<storage-plugin-name>-<param-name>
# Make sure that all defined fields are 'Optional' and specify a default value
# of None or anything else that makes sense in your case.
# Note that we allow storage plugin settings to be tagged by the user. That means,
# that each of them can be specified multiple times (an implicit nargs=+), and
# the user can add a tag in front of each value (e.g. tagname1:value1 tagname2:value2).
# This way, a storage plugin can be used multiple times within a workflow with different
# settings.


# Copy the available settings over from the Rucio client.
_RUCIO_CLIENT_CLS = rucio.client.baseclient.BaseClient


def _get_help(arg: str) -> str:
    """Read the help text for a Rucio client argument."""
    doc = _RUCIO_CLIENT_CLS.__init__.__doc__
    match = re.search(f"\n{arg} +:\n +(?P<txt>.*)\n", doc)
    if not match:
        # The help text is in a different format for versions of rucio before 37.4:
        match = re.search(f"\n:param +{arg}: +(?P<txt>.*)\n", doc)
    return match.group("txt") if match else ""


StorageProviderSettings = dataclasses.make_dataclass(
    "StorageProviderSettings",
    fields=[
        (
            f.name,
            f.annotation,
            dataclasses.field(
                default=f.default,
                metadata={"help": _get_help(f.name)},
            ),
        )
        for f in inspect.signature(_RUCIO_CLIENT_CLS).parameters.values()
        if f.name not in ("logger",)
    ]
    + [
        (
            "ignore_checksum",
            bool,
            dataclasses.field(
                default=False,
                metadata={
                    "help": "If true, skips the checksum validation between the downloaded file and the rucio catalogue.",
                },
            ),
        ),
        (
            "download_rse",
            str,
            dataclasses.field(
                default=None,
                metadata={
                    "help": "Rucio Storage Element (RSE) expression to download files from.",
                },
            ),
        ),
        (
            "upload_rse",
            str,
            dataclasses.field(
                default=None,
                metadata={
                    "help": "Rucio Storage Element (RSE) expression to upload files to.",
                },
            ),
        ),
        (
            "upload_dataset",
            str,
            dataclasses.field(
                default=None,
                metadata={
                    "help": "Rucio dataset to attach files to on upload.",
                },
            ),
        ),
        (
            "cache_scope",
            bool,
            dataclasses.field(
                default=False,
                metadata={
                    "help": "If true, minimize the number of server calls by caching the size and creation time of all files in the same scope.",
                },
            ),
        ),
    ],
    bases=(StorageProviderSettingsBase,),
)


class StorageProvider(StorageProviderBase):
    """Rucio storage provider."""

    # For compatibility with future changes, you should not overwrite the __init__
    # method. Instead, use __post_init__ to set additional attributes and initialize
    # further stuff.

    def __post_init__(self) -> None:
        """Initialize the storage provider."""
        # This is optional and can be removed if not needed.
        # Alternatively, you can e.g. prepare a connection to your storage backend here.
        # and set additional attributes.
        valid_client_args = inspect.signature(_RUCIO_CLIENT_CLS).parameters
        client_kwargs = {
            k: v
            for k, v in dataclasses.asdict(self.settings).items()
            if k in valid_client_args
        }

        logger = get_logger()
        self.client = rucio.client.Client(logger=logger, **client_kwargs)
        self.dclient = rucio.client.downloadclient.DownloadClient(
            self.client, logger=logger
        )
        self.uclient = rucio.client.uploadclient.UploadClient(
            self.client, logger=logger
        )

    @classmethod
    def example_queries(cls) -> list[ExampleQuery]:
        """Return example queries with description for this storage provider."""
        return [
            ExampleQuery(
                query="rucio://myscope/myfile.txt",
                type=QueryType.ANY,
                description='The file "myfile.txt" in Rucio scope "myscope".',
            ),
        ]

    def rate_limiter_key(
        self,
        query: str,  # noqa: ARG002
        operation: Operation,  # noqa: ARG002
    ) -> str:
        """Return a key for identifying a rate limiter given a query and an operation.

        This is used to identify a rate limiter for the query.
        E.g. for a storage provider like http that would be the host name.
        For s3 it might be just the endpoint URL.
        """
        return self.settings.rucio_host

    def default_max_requests_per_second(self) -> float:
        """Return the default maximum number of requests per second."""
        return 100

    def use_rate_limiter(self) -> bool:
        """Return False if no rate limiting is needed for this provider."""
        return False

    @classmethod
    def is_valid_query(cls, query: str) -> StorageQueryValidationResult:
        """Return whether the given query is valid for this storage provider."""
        # Ensure that also queries containing wildcards (e.g. {sample}) are accepted
        # and considered valid. The wildcards will be resolved before the storage
        # object is actually used.
        try:
            parsed = urlparse(query)
        except Exception as exc:  # noqa: BLE001
            return StorageQueryValidationResult(
                query=query,
                valid=False,
                reason=f"cannot be parsed as URL ({exc})",
            )

        if parsed.scheme in ("rucio", ""):
            # Acceptable forms:
            # - rucio://scope/file
            # - rucio:/scope/file
            # - /scope/file
            # - scope/file
            path_elements = [p for p in parsed.path.strip("/").split("/") if p]
            if (bool(parsed.netloc) and len(path_elements) == 1) or (
                not parsed.netloc and len(path_elements) == 2  # noqa: PLR2004
            ):
                return StorageQueryValidationResult(
                    query=query,
                    valid=True,
                )
        elif parsed.scheme and parsed.netloc:
            # Accept any valid URL, to be used when retrieve=False.
            return StorageQueryValidationResult(
                query=query,
                valid=True,
            )

        return StorageQueryValidationResult(
            query=query,
            valid=False,
            reason="must be of the form rucio://scope/file",
        )


class StorageObject(StorageObjectRead, StorageObjectWrite, StorageObjectGlob):
    """Rucio storage object. This represents a single file in Rucio."""

    # For compatibility with future changes, you should not overwrite the __init__
    # method. Instead, use __post_init__ to set additional attributes and initialize
    # further stuff.

    def __post_init__(self) -> None:
        """Initialize the storage object."""
        self.query: str
        if not self.is_valid_query():
            raise ValueError(self.query)
        parsed = urlparse(self.query)
        if parsed.scheme in ("rucio", ""):
            # Acceptable forms:
            # - rucio://scope/file
            # - rucio:/scope/file
            # - /scope/file
            # - scope/file
            path_elements = parsed.path.lstrip("/").split("/")
            if parsed.netloc:
                self.scope = parsed.netloc
                self.file = path_elements[0]
            else:
                self.scope, self.file = path_elements
        else:
            # When retrieve=False, the query is set to a URL and there is no
            # way to extract the scope and file from it.
            self.scope = ""
            self.file = ""

        if not self.retrieve:
            streaming_url = self._get_streaming_url()
            if streaming_url is not None:
                # The snakemake code assumes that the query is equal to the
                # remote path when retrieve is set to False.
                # While this works for https and s3, it does not work for Rucio
                # because the Rucio query is not a a valid URL and the tools that
                # use the streaming URL are not aware of Rucio.
                # https://github.com/snakemake/snakemake/blob/6dee2b55fbfff3bdad33cecdbeb8bd55ff4586bc/src/snakemake/io/__init__.py#L1752-L1761
                # Therefore, we set the query to the streaming URL.
                self.query = streaming_url
                # When a job fails, it is displayed using the local_path(),
                # even though the path in the job script as executed is the query (see above).
                # Therefore, we set the local path to the streaming URL for easy
                # to understand error messages.
                self.set_local_path(streaming_url)

    @property
    def client(self) -> rucio.client.Client:
        """Rucio client."""
        return self.provider.client

    async def inventory(self, cache: IOCacheStorageInterface) -> None:
        """Read the information about all files in a scope efficiently.

        From this file, try to find as much existence and modification date
        information as possible. Only retrieve that information that comes for free
        given the current object.
        """
        # If this is implemented in a storage object, results have to be stored in
        # the given IOCache object, using self.cache_key() as key.
        # Optionally, this can take a custom local suffix, needed e.g. when you want
        # to cache more items than the current query: self.cache_key(local_suffix=...)
        if not self.retrieve:
            return

        if self.get_inventory_parent() in cache.exists_in_storage:
            # record has been inventorized before
            return

        # This retrieves information about all the files in the file scope at
        # once. This is faster than sending a new request for each file, but
        # If this becomes too slow because scopes contain too many files,
        # we may need to add a setting to disable it.
        if self.provider.settings.cache_scope:
            # Cache the entire scope
            if self.scope not in self.client.list_scopes():
                # check if scope exists
                cache.exists_in_storage[self.cache_key()] = False
            else:
                cache.exists_in_storage[self.get_inventory_parent()] = True
                files = self.client.list_dids(
                    scope=self.scope,
                    filters=[{"type": "file"}],
                )
                batch_size = 500
                batch = []
                for i, file in enumerate(files, 1):
                    batch.append(file)
                    if i % batch_size == 0:
                        self._handle(cache, batch)
                        batch.clear()
                self._handle(cache, batch)
        else:
            self._handle(cache, [self.file])

    def _handle(self, cache: IOCacheStorageInterface, files: Sequence[str]) -> None:
        """Add a sequence of files to the cache."""
        dids = [{"scope": self.scope, "name": f} for f in files]
        for file, meta in zip(files, self.client.get_metadata_bulk(dids), strict=True):
            key = self.cache_key(f"{self.scope}/{file}")
            cache.mtime[key] = Mtime(storage=meta["updated_at"].timestamp())
            cache.size[key] = meta["bytes"]
            cache.exists_in_storage[key] = True

    def get_inventory_parent(self) -> str:
        """Return the parent directory of this object."""
        return self.scope

    def local_suffix(self) -> str:
        """Return a unique suffix for the local path, determined from self.query."""
        return f"{self.scope}/{self.file}"

    def cleanup(self) -> None:
        """Perform local cleanup of any remainders of the storage object."""
        # self.local_path() should not be removed, as this is taken care of by
        # Snakemake.

    # Fallible methods should implement some retry logic.
    # The easiest way to do this (but not the only one) is to use the retry_decorator
    # provided by snakemake-interface-storage-plugins.
    @retry_decorator
    def exists(self) -> bool:
        """Return True if the object exists."""
        try:
            self.client.get_did(scope=self.scope, name=self.file)
        except rucio.common.exception.DataIdentifierNotFound:
            return False
        return True

    @retry_decorator
    def mtime(self) -> float:
        """Return the modification time."""
        meta = self.client.get_metadata(scope=self.scope, name=self.file)
        return meta["updated_at"].timestamp()

    @retry_decorator
    def size(self) -> int:
        """Return the size in bytes."""
        did = self.client.get_did(scope=self.scope, name=self.file)
        return did["bytes"]

    @retry_decorator
    def _get_streaming_url(self) -> str | None:
        """Return a URL for streaming the file."""
        replicas = self.client.list_replicas(
            dids=[{"scope": self.scope, "name": self.file}],
            rse_expression=self.provider.settings.download_rse,
        )
        urls = [
            url
            for replica in replicas
            for site_urls in replica["rses"].values()
            for url in site_urls
        ]
        return random.choice(urls) if urls else None  # noqa: S311

    @retry_decorator
    def retrieve_object(self) -> None:
        """Download the file to self.local_path()."""
        self.provider.dclient.download_dids(
            [
                {
                    "base_dir": self.local_path().parent,
                    "did": f"{self.scope}:{self.file}",
                    "ignore_checksum": self.provider.settings.ignore_checksum,
                    "no_subdir": True,
                    "rse": self.provider.settings.download_rse,
                },
            ],
            num_threads=1,
        )

    def store_object(self) -> None:
        """Upload the file."""
        if self.exists():
            msg = f'File "{self.scope}/{self.file}" already exists on Rucio'
            raise ValueError(msg)
        if self.provider.settings.upload_rse is None:
            msg = "Please specify the `upload_rse`."
            raise ValueError(msg)
        if self.provider.settings.upload_dataset is None:
            msg = "Please specify the `upload_dataset`."
            raise ValueError(msg)
        self._store_object()

    @retry_decorator
    def _store_object(self) -> None:
        """Upload the file."""
        self.provider.uclient.upload(
            [
                {
                    "path": self.local_path(),
                    "did_scope": self.scope,
                    "dataset_scope": self.scope,
                    "dataset_name": self.provider.settings.upload_dataset,
                    "rse": self.provider.settings.upload_rse,
                    "register_after_upload": True,
                },
            ],
        )

    def remove(self) -> None:
        """Remove the file from the storage."""
        msg = "Rucio does not support deleting files."
        raise NotImplementedError(msg)

    @retry_decorator
    def list_candidate_matches(self) -> Iterable[str]:
        """Return a list of candidate matches in the storage for the query."""
        # This is used by glob_wildcards() to find matches for wildcards in the query.
        # The method has to return concretized queries without any remaining wildcards.
        # Use snakemake_executor_plugins.io.get_constant_prefix(self.query) to get the
        # prefix of the query before the first wildcard.
        return self.client.list_dids(
            scope=self.scope,
            filters=[
                {
                    "name": self.file,
                    "type": "file",
                }
            ],
        )
