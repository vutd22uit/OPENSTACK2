"""
Business logic service layer
"""
from app.models.data_model import DataModel
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class DataService:
    """Service for data operations"""

    def __init__(self):
        # In production, this would connect to a database
        self._data_store = []
        self._next_id = 1

    def get_paginated_data(self, page: int, limit: int) -> dict:
        """Get paginated data"""
        start = (page - 1) * limit
        end = start + limit

        items = self._data_store[start:end]

        return {
            'data': [item.to_dict() for item in items],
            'page': page,
            'limit': limit,
            'total': len(self._data_store)
        }

    def get_by_id(self, data_id: int) -> Optional[dict]:
        """Get data by ID"""
        for item in self._data_store:
            if item.id == data_id:
                return item.to_dict()
        return None

    def create_data(self, data: dict) -> dict:
        """Create new data"""
        try:
            new_item = DataModel(
                id=self._next_id,
                name=data['name'],
                description=data['description']
            )

            # Validate before saving
            new_item.validate()

            self._data_store.append(new_item)
            self._next_id += 1

            logger.info(f"Created new data with ID: {new_item.id}")

            return new_item.to_dict()

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error creating data: {str(e)}")
            raise

    def delete_by_id(self, data_id: int) -> bool:
        """Delete data by ID"""
        for i, item in enumerate(self._data_store):
            if item.id == data_id:
                self._data_store.pop(i)
                logger.info(f"Deleted data with ID: {data_id}")
                return True
        return False
