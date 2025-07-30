"""Domain services for BM25 operations."""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from kodit.domain.value_objects import (
    BM25DeleteRequest,
    BM25IndexRequest,
    BM25SearchRequest,
    BM25SearchResult,
)


class BM25Repository(ABC):
    """Abstract interface for BM25 repository."""

    @abstractmethod
    async def index_documents(self, request: BM25IndexRequest) -> None:
        """Index documents for BM25 search."""

    @abstractmethod
    async def search(self, request: BM25SearchRequest) -> Sequence[BM25SearchResult]:
        """Search documents using BM25."""

    @abstractmethod
    async def delete_documents(self, request: BM25DeleteRequest) -> None:
        """Delete documents from the BM25 index."""


class BM25DomainService:
    """Domain service for BM25 operations."""

    def __init__(self, repository: BM25Repository) -> None:
        """Initialize the BM25 domain service.

        Args:
            repository: The BM25 repository for persistence operations

        """
        self.repository = repository

    async def index_documents(self, request: BM25IndexRequest) -> None:
        """Index documents using domain business rules.

        Args:
            request: The indexing request containing documents to index

        Raises:
            ValueError: If the request is invalid

        """
        # Domain logic: validate request
        if not request.documents:
            raise ValueError("Cannot index empty document list")

        # Domain logic: filter out invalid documents
        valid_documents = [
            doc
            for doc in request.documents
            if doc.snippet_id is not None and doc.text and doc.text.strip()
        ]

        if not valid_documents:
            raise ValueError("No valid documents to index")

        # Domain logic: create new request with validated documents
        validated_request = BM25IndexRequest(documents=valid_documents)
        await self.repository.index_documents(validated_request)

    async def search(self, request: BM25SearchRequest) -> Sequence[BM25SearchResult]:
        """Search documents using domain business rules.

        Args:
            request: The search request

        Returns:
            Sequence of search results

        Raises:
            ValueError: If the request is invalid

        """
        # Domain logic: validate request
        if not request.query or not request.query.strip():
            raise ValueError("Search query cannot be empty")

        if request.top_k <= 0:
            raise ValueError("Top-k must be positive")

        # Domain logic: normalize query
        normalized_query = request.query.strip()
        normalized_request = BM25SearchRequest(
            query=normalized_query, top_k=request.top_k
        )

        return await self.repository.search(normalized_request)

    async def delete_documents(self, request: BM25DeleteRequest) -> None:
        """Delete documents using domain business rules.

        Args:
            request: The deletion request

        Raises:
            ValueError: If the request is invalid

        """
        # Domain logic: validate request
        if not request.snippet_ids:
            raise ValueError("Cannot delete empty snippet ID list")

        # Domain logic: filter out invalid IDs
        valid_ids = [
            snippet_id
            for snippet_id in request.snippet_ids
            if snippet_id is not None and snippet_id > 0
        ]

        if not valid_ids:
            raise ValueError("No valid snippet IDs to delete")

        # Domain logic: create new request with validated IDs
        validated_request = BM25DeleteRequest(snippet_ids=valid_ids)
        await self.repository.delete_documents(validated_request)
