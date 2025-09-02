"""
Material model for landscaping materials
"""

from sqlalchemy import Column, String, Text, DECIMAL, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import db
import enum
import uuid

class MaterialType(enum.Enum):
    BLOCK = "block"
    STONE = "stone"
    BRICK = "brick"
    CONCRETE = "concrete"
    WOOD = "wood"
    METAL = "metal"
    OTHER = "other"

class Material(db.Model):
    __tablename__ = 'materials'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    material_type = Column(String(50), nullable=False)  # Use String instead of Enum
    description = Column(Text)
    length_inches = Column(DECIMAL(8, 2))
    width_inches = Column(DECIMAL(8, 2))
    height_inches = Column(DECIMAL(8, 2))
    weight_lbs = Column(DECIMAL(8, 2))
    price_per_unit = Column(DECIMAL(10, 2), nullable=False)
    unit_of_measure = Column(String(50), default='each')
    supplier = Column(String(255))
    supplier_part_number = Column(String(100))
    use_case = Column(Text)
    installation_notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'material_type': self.material_type,
            'description': self.description,
            'length_inches': float(self.length_inches) if self.length_inches else None,
            'width_inches': float(self.width_inches) if self.width_inches else None,
            'height_inches': float(self.height_inches) if self.height_inches else None,
            'weight_lbs': float(self.weight_lbs) if self.weight_lbs else None,
            'price_per_unit': float(self.price_per_unit),
            'unit_of_measure': self.unit_of_measure,
            'supplier': self.supplier,
            'supplier_part_number': self.supplier_part_number,
            'use_case': self.use_case,
            'installation_notes': self.installation_notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
