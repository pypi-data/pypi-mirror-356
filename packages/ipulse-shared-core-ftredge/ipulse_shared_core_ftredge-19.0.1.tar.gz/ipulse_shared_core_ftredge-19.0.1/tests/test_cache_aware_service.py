"""Tests for the CacheAwareFirestoreService."""

import pytest
import logging
from unittest.mock import MagicMock, patch
from pydantic import BaseModel
from ipulse_shared_core_ftredge.cache.shared_cache import SharedCache
from ipulse_shared_core_ftredge.services import CacheAwareFirestoreService
from ipulse_shared_core_ftredge.models.base_data_model import BaseDataModel


# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create a simple model for testing that extends BaseDataModel
class CacheTestModel(BaseDataModel):
    VERSION = 1.0
    DOMAIN = "test"
    OBJ_REF = "cache_test_model"

    id: str
    name: str
    description: str


class TestCacheAwareFirestoreService:
    """Test cases for CacheAwareFirestoreService."""

    @pytest.fixture
    def service(self):
        """Set up test fixtures."""
        # Create mock Firestore client
        db_mock = MagicMock()

        # Create mock caches
        document_cache = SharedCache[dict](
            name="TestDocCache",
            ttl=1.0,
            enabled=True,
            logger=logger
        )

        collection_cache = SharedCache[list](
            name="TestCollectionCache",
            ttl=1.0,
            enabled=True,
            logger=logger
        )

        # Create service instance with mocks
        service = CacheAwareFirestoreService[CacheTestModel](
            db=db_mock,
            collection_name="test_collection",
            resource_type="test_resource",
            logger=logger,
            document_cache=document_cache,
            collection_cache=collection_cache,
            timeout=5.0
        )

        return service

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.get_document')
    async def test_get_document_cache_hit(self, mock_get_document, service):
        """Test get_document with cache hit."""
        # Prepare cached data
        test_data = {"id": "doc123", "name": "Test Doc", "description": "This is a test"}
        service.document_cache.set("doc123", test_data)

        # Execute get_document
        result = await service.get_document("doc123")

        # Verify result comes from cache
        assert result == test_data

        # Verify Firestore was not called
        mock_get_document.assert_not_called()

    @patch('google.cloud.firestore.Client')
    async def test_get_document_cache_miss(self, mock_firestore_client, service):
        """Test get_document with cache miss."""
        # Configure mock to return data
        mock_doc = MagicMock()
        mock_doc.exists = True
        mock_doc.to_dict.return_value = {"id": "doc123", "name": "Test Doc", "description": "This is a test"}

        mock_doc_ref = MagicMock()
        mock_doc_ref.get.return_value = mock_doc

        service.db.collection.return_value.document.return_value = mock_doc_ref

        # Execute get_document
        result = await service.get_document("doc123")

        # Verify Firestore was called
        service.db.collection.assert_called_with("test_collection")
        service.db.collection.return_value.document.assert_called_with("doc123")

        # Verify result is correct
        expected_data = {"id": "doc123", "name": "Test Doc", "description": "This is a test"}
        assert result == expected_data

        # Verify data was cached
        cached_data = service.document_cache.get("doc123")
        assert cached_data == expected_data

    async def test_get_all_documents_cache_hit(self, service):
        """Test get_all_documents with cache hit."""
        # Prepare cached data
        test_docs = [
            {"id": "doc1", "name": "Doc 1", "description": "First doc"},
            {"id": "doc2", "name": "Doc 2", "description": "Second doc"}
        ]
        service.collection_cache.set("test_cache_key", test_docs)

        # Execute get_all_documents
        result = await service.get_all_documents("test_cache_key")

        # Verify result comes from cache
        assert result == test_docs

    @patch('google.cloud.firestore.Client')
    async def test_get_all_documents_cache_miss(self, mock_firestore_client, service):
        """Test get_all_documents with cache miss."""
        # Configure mock to return documents
        mock_doc1 = MagicMock()
        mock_doc1.id = "doc1"
        mock_doc1.to_dict.return_value = {"name": "Doc 1", "description": "First doc"}

        mock_doc2 = MagicMock()
        mock_doc2.id = "doc2"
        mock_doc2.to_dict.return_value = {"name": "Doc 2", "description": "Second doc"}

        service.db.collection.return_value.stream.return_value = [mock_doc1, mock_doc2]

        # Execute get_all_documents
        result = await service.get_all_documents("test_cache_key")

        # Verify Firestore was called
        service.db.collection.assert_called_with("test_collection")

        # Verify result is correct
        expected_docs = [
            {"id": "doc1", "name": "Doc 1", "description": "First doc"},
            {"id": "doc2", "name": "Doc 2", "description": "Second doc"}
        ]
        assert result == expected_docs

        # Verify documents were cached
        cached_docs = service.collection_cache.get("test_cache_key")
        assert cached_docs == expected_docs

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.update_document')
    async def test_update_document_invalidates_cache(self, mock_update, service):
        """Test that update_document invalidates relevant caches."""
        # Pre-populate caches
        service.document_cache.set("doc123", {"id": "doc123", "name": "Old Doc"})
        service.collection_cache.set("all_documents", [{"id": "doc123", "name": "Old Doc"}])

        # Execute update
        updated_data = {"id": "doc123", "name": "Updated Doc", "description": "This was updated"}
        await service.update_document("doc123", updated_data, "user123")

        # Verify caches were invalidated
        assert service.document_cache.get("doc123") is None
        assert service.collection_cache.get("all_documents") is None

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.create_document')
    async def test_create_document_invalidates_cache(self, mock_create, service):
        """Test that create_document invalidates collection cache."""
        # Pre-populate collection cache
        service.collection_cache.set("all_documents", [{"id": "doc1", "name": "Doc 1"}])

        # Execute create with properly initialized model
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        new_model = CacheTestModel(
            id="doc2",
            name="New Doc",
            description="Newly created",
            schema_version=1.0,
            created_at=now,
            created_by="user123",
            updated_at=now,
            updated_by="user123"
        )
        await service.create_document("doc2", new_model, "user123")

        # Verify collection cache was invalidated
        assert service.collection_cache.get("all_documents") is None

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.delete_document')
    async def test_delete_document_invalidates_cache(self, mock_delete, service):
        """Test that delete_document invalidates relevant caches."""
        # Pre-populate caches
        test_docs = [{"id": "doc123", "name": "Doc to Delete"}]
        service.document_cache.set("doc123", test_docs[0])
        service.collection_cache.set("all_documents", test_docs)

        # Execute delete
        await service.delete_document("doc123")

        # Verify caches were invalidated
        assert service.document_cache.get("doc123") is None
        assert service.collection_cache.get("all_documents") is None

    def test_invalidate_document_cache(self, service):
        """Test _invalidate_document_cache method."""
        # Pre-populate cache
        service.document_cache.set("doc123", {"id": "doc123", "name": "Test Doc"})

        # Execute invalidation
        service._invalidate_document_cache("doc123")

        # Verify cache was cleared
        assert service.document_cache.get("doc123") is None

    def test_invalidate_collection_cache(self, service):
        """Test _invalidate_collection_cache method."""
        # Pre-populate cache with specific key
        cache_key_to_invalidate = "test_collection_cache"
        service.collection_cache.set(cache_key_to_invalidate, [{"id": "doc1"}])

        # Execute invalidation
        service._invalidate_collection_cache(cache_key_to_invalidate)

        # Verify cache was cleared
        assert service.collection_cache.get(cache_key_to_invalidate) is None

    def test_invalidate_collection_cache_custom_key(self, service):
        """Test _invalidate_collection_cache method with custom key."""
        # Pre-populate cache with custom key
        service.collection_cache.set("custom_key", [{"id": "doc1"}])

        # Execute invalidation with custom key
        service._invalidate_collection_cache("custom_key")

        # Verify cache was cleared
        assert service.collection_cache.get("custom_key") is None

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.archive_document')
    async def test_archive_document_invalidates_cache(self, mock_archive, service):
        """Test that archive_document invalidates relevant caches."""
        # Pre-populate caches
        service.document_cache.set("doc123", {"id": "doc123", "name": "Test Doc"})
        service.collection_cache.set("all_documents", [{"id": "doc123", "name": "Test Doc"}])

        # Execute archive
        document_data = {"id": "doc123", "name": "Test Doc", "description": "Archive me"}
        await service.archive_document(document_data, "doc123", "archive_collection", "user123")

        # Verify caches were invalidated
        assert service.document_cache.get("doc123") is None
        assert service.collection_cache.get("all_documents") is None

    @patch('ipulse_shared_core_ftredge.services.BaseFirestoreService.restore_document')
    async def test_restore_document_invalidates_cache(self, mock_restore, service):
        """Test that restore_document invalidates relevant caches."""
        # Pre-populate caches
        service.document_cache.set("doc123", {"id": "doc123", "name": "Old Doc"})
        service.collection_cache.set("all_documents", [{"id": "doc123", "name": "Old Doc"}])

        # Execute restore
        await service.restore_document("doc123", "archive_collection", "target_collection", "user123")

        # Verify caches were invalidated
        assert service.document_cache.get("doc123") is None
        assert service.collection_cache.get("all_documents") is None
