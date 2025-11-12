"""
Data models with validation
"""
from datetime import datetime
from typing import Optional

class DataModel:
    """Data model with built-in validation"""

    def __init__(self, id: int, name: str, description: str,
                 created_at: Optional[datetime] = None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create model from dictionary"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            created_at=data.get('created_at')
        )

    def validate(self):
        """Validate model data"""
        if not self.name or len(self.name) > 100:
            raise ValueError("Invalid name: must be 1-100 characters")

        if not self.description or len(self.description) > 500:
            raise ValueError("Invalid description: must be 1-500 characters")

        return True
