from __future__ import annotations

from typing import IO, Any

from verse.core import Response, operation
from verse.internal.storage_core import CollectionResult, StoreComponent
from verse.ql import Expression, Value

from ._models import (
    ObjectBatch,
    ObjectCollectionConfig,
    ObjectItem,
    ObjectKey,
    ObjectList,
    ObjectProperties,
    ObjectQueryConfig,
    ObjectSource,
    ObjectTransferConfig,
)


class ObjectStore(StoreComponent):
    collection: str | None

    def __init__(self, collection: str | None = None, **kwargs):
        """Initialize.

        Args:
            collection:
                Collection name.
        """
        self.collection = collection
        super().__init__(**kwargs)

    @operation()
    def create_collection(
        self,
        collection: str | None = None,
        config: dict | ObjectCollectionConfig | None = None,
        where: str | Expression | None = None,
        **kwargs: Any,
    ) -> Response[CollectionResult]:
        """Create collection.

        Args:
            collection:
                Collection name.
            config:
                Collection config.
            where:
                Condition expression.

        Returns:
            Collection operation result.
        """
        ...

    @operation()
    def drop_collection(
        self,
        collection: str | None = None,
        where: str | Expression | None = None,
        **kwargs: Any,
    ) -> Response[CollectionResult]:
        """Drop collection.

        Args:
            collection:
                Collection name.
            where:
                Condition expression.

        Returns:
            Collection operation result.
        """
        ...

    @operation()
    def list_collections(
        self,
        **kwargs: Any,
    ) -> Response[list[str]]:
        """List collections.

        Returns:
            List of collection names.
        """
        ...

    @operation()
    def has_collection(
        self,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[bool]:
        """Check if the collection exists.

        Args:
            collection:
                Collection name.

        Returns:
            A value indicating whether the collection exists.
        """
        ...

    @operation()
    def put(
        self,
        key: str | dict | ObjectKey,
        value: Value = None,
        file: str | None = None,
        stream: IO | None = None,
        metadata: dict | None = None,
        properties: dict | ObjectProperties | None = None,
        where: str | Expression | None = None,
        config: dict | ObjectTransferConfig | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Put object.

        Args:
            key:
                Object key.
            value:
                Object value. If the type is not bytes, it
                will be converted to bytes.
            file:
                File path to upload.
            stream:
                Stream to upload.
            metadata:
                Custom metadata.
            properties:
                Object properties.
            where:
                Condition expression.
            config:
                Transfer config.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            PreconditionFailedError:
                Condition failed.
        """
        ...

    @operation()
    def get(
        self,
        key: str | dict | ObjectKey,
        file: str | None = None,
        stream: IO | None = None,
        where: str | Expression | None = None,
        start: int | None = None,
        end: int | None = None,
        config: dict | ObjectTransferConfig | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object.

        Args:
            key:
                Object key.
            file:
                File path to download.
            stream:
                Stream to download to.
            where:
                Condition expression.
            start:
                Start bytes for range request.
            end:
                End bytes for range request.
            config:
                Transfer config.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        ...

    @operation()
    def get_metadata(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object metadata.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item with metadata.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        ...

    @operation()
    def get_properties(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object properties.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item with properties.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        ...

    @operation()
    def get_versions(
        self,
        key: str | dict | ObjectKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object versions.

        Args:
            key:
                Object key.
            collection:
                Collection name.

        Returns:
            Object item with object versions.

        Raises:
            NotFoundError:
                Object not found.
        """
        ...

    @operation()
    def update(
        self,
        key: str | dict | ObjectKey,
        metadata: dict | None = None,
        properties: dict | ObjectProperties | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Update object metadata and properties.

        Args:
            key:
                Objecy key.
            metadata:
                Custom metadata.
            properties:
                Object properties.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            NotFoundError:
                Object not found.
            PreconditionFailedError:
                Condition failed.
        """
        ...

    @operation()
    def delete(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete object.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            None.

        Raises:
            NotFoundError:
                Object not found.
            PreconditionFailedError:
                Condition failed.
        """
        ...

    @operation()
    def copy(
        self,
        key: str | dict | ObjectKey,
        source: str | dict | ObjectSource,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Copy object.

        Args:
            key:
                Destination object key.
            source:
                Object source.
            collection:
                Collection name.

        Returns:
            Copied object item.

        Raises:
            NotFoundError:
                Source object not found.
        """
        ...

    @operation()
    def generate(
        self,
        key: str | dict | ObjectKey,
        method: str,
        expiry: int,
        collection: str | None = None,
    ) -> Response[ObjectItem]:
        """Generate signed URL.

        Args:
            key:
                Object key.
            method:
                Operation method. One of "GET", "PUT" or "DELETE".
            expiry:
                Expiry in milliseconds.
            collection:
                Collection name.

        Returns:
            Object item with signed URL.
        """
        ...

    @operation()
    def query(
        self,
        where: str | Expression | None = None,
        limit: int | None = None,
        continuation: str | None = None,
        config: dict | ObjectQueryConfig | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[ObjectList]:
        """Query objects.

        Args:
            where:
                Condition expression.
            limit:
                Query limit.
            continuation:
                Continuation token.
            config:
                Query config.
            collection:
                Collection name.

        Returns:
            List of objects.
        """
        ...

    @operation()
    def count(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count objects.

        Args:
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Count of objects.
        """
        ...

    @operation()
    def batch(
        self,
        batch: dict | ObjectBatch,
        **kwargs,
    ) -> Response[list[Any]]:
        """Batch operation.

        Args:
            batch:
                Object batch.

        Returns:
            Batch operation results.
        """
        ...

    @operation()
    def close(
        self,
        **kwargs: Any,
    ) -> Response[None]:
        """Close the sync client.

        Returns:
            None.
        """
        ...

    @operation()
    async def acreate_collection(
        self,
        collection: str | None = None,
        config: dict | ObjectCollectionConfig | None = None,
        **kwargs: Any,
    ) -> Response[CollectionResult]:
        """Create collection.

        Args:
            collection:
                Collection name.
            config:
                Collection config.

        Returns:
            Collection operation result.
        """
        ...

    @operation()
    async def adrop_collection(
        self,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[CollectionResult]:
        """Drop collection.

        Args:
            collection:
                Collection name.

        Returns:
            Collection operation result.
        """
        ...

    @operation()
    async def alist_collections(
        self,
        **kwargs: Any,
    ) -> Response[list[str]]:
        """List collections.

        Returns:
            List of collection names.
        """
        ...

    @operation()
    async def ahas_collection(
        self,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[bool]:
        """Check if the collection exists.

        Args:
            collection:
                Collection name.

        Returns:
            A value indicating whether the collection exists.
        """
        ...

    @operation()
    async def aput(
        self,
        key: str | dict | ObjectKey,
        value: Value = None,
        file: str | None = None,
        stream: IO | None = None,
        metadata: dict | None = None,
        properties: dict | ObjectProperties | None = None,
        where: str | Expression | None = None,
        config: dict | ObjectTransferConfig | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Put object.

        Args:
            key:
                Object key.
            value:
                Object value. If the type is not bytes, it
                will be converted to bytes.
            file:
                File path to upload.
            stream:
                Stream to upload.
            metadata:
                Custom metadata.
            properties:
                Object properties.
            where:
                Condition expression.
            config:
                Transfer config.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            PreconditionFailedError:
                Condition failed.
        """
        ...

    @operation()
    async def aget(
        self,
        key: str | dict | ObjectKey,
        file: str | None = None,
        stream: IO | None = None,
        where: str | Expression | None = None,
        start: int | None = None,
        end: int | None = None,
        config: dict | ObjectTransferConfig | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object.

        Args:
            key:
                Object key.
            file:
                File path to download.
            stream:
                Stream to download to.
            where:
                Condition expression.
            start:
                Start bytes for range request.
            end:
                End bytes for range request.
            config:
                Transfer config.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        ...

    @operation()
    async def aget_metadata(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object metadata.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item with metadata.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        ...

    @operation()
    async def aget_properties(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object properties.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item with properties.

        Raises:
            NotFoundError:
                Object not found.
            NotModified:
                Object not modified.
        """
        ...

    @operation()
    async def aget_versions(
        self,
        key: str | dict | ObjectKey,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Get object versions.

        Args:
            key:
                Object key.
            collection:
                Collection name.

        Returns:
            Object item with object versions.

        Raises:
            NotFoundError:
                Object not found.
        """
        ...

    @operation()
    async def aupdate(
        self,
        key: str | dict | ObjectKey,
        metadata: dict | None = None,
        properties: dict | ObjectProperties | None = None,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Update object metadata and properties.

        Args:
            key:
                Objecy key.
            metadata:
                Custom metadata.
            properties:
                Object properties.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Object item.

        Raises:
            NotFoundError:
                Object not found.
            PreconditionFailedError:
                Condition failed.
        """
        ...

    @operation()
    async def adelete(
        self,
        key: str | dict | ObjectKey,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[None]:
        """Delete object.

        Args:
            key:
                Object key.
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            None.

        Raises:
            NotFoundError:
                Object not found.
            PreconditionFailedError:
                Condition failed.
        """
        ...

    @operation()
    async def acopy(
        self,
        key: str | dict | ObjectKey,
        source: str | dict | ObjectSource,
        collection: str | None = None,
        **kwargs: Any,
    ) -> Response[ObjectItem]:
        """Copy object.

        Args:
            key:
                Destination object key.
            source:
                Object source.
            collection:
                Collection name.

        Returns:
            Copied object item.

        Raises:
            NotFoundError:
                Source object not found.
        """
        ...

    @operation()
    async def agenerate(
        self,
        key: str | dict | ObjectKey,
        method: str,
        expiry: int,
        collection: str | None = None,
    ) -> Response[ObjectItem]:
        """Generate signed URL.

        Args:
            key:
                Object key.
            method:
                Operation method. One of "GET", "PUT" or "DELETE".
            expiry:
                Expiry in milliseconds.
            collection:
                Collection name.

        Returns:
            Object item with signed URL.
        """
        ...

    @operation()
    async def aquery(
        self,
        where: str | Expression | None = None,
        limit: int | None = None,
        continuation: str | None = None,
        config: dict | ObjectQueryConfig | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[ObjectList]:
        """Query objects.

        Args:
            where:
                Condition expression.
            limit:
                Query limit.
            continuation:
                Continuation token.
            config:
                Query config.
            collection:
                Collection name.

        Returns:
            List of objects.
        """
        ...

    @operation()
    async def acount(
        self,
        where: str | Expression | None = None,
        collection: str | None = None,
        **kwargs,
    ) -> Response[int]:
        """Count objects.

        Args:
            where:
                Condition expression.
            collection:
                Collection name.

        Returns:
            Count of objects.
        """
        ...

    @operation()
    async def abatch(
        self,
        batch: dict | ObjectBatch,
        **kwargs,
    ) -> Response[list[Any]]:
        """Batch operation.

        Args:
            operations:
                Object batch.

        Returns:
            Batch operation results.
        """
        ...

    @operation()
    async def aclose(
        self,
        **kwargs: Any,
    ) -> Response[None]:
        """Close the async client.

        Returns:
            None.
        """
        ...
