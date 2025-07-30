"""
Base service classes for ipulse_shared_core_ftredge

This module provides base service classes without importing any concrete services,
preventing circular import dependencies.
"""

from .base_firestore_service import BaseFirestoreService

__all__ = [
    'BaseFirestoreService'
]
