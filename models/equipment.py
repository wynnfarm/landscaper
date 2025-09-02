"""
Equipment model for landscaping equipment
"""

from sqlalchemy import Column, String, Text, DECIMAL, Boolean, DateTime, Date, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import db
import enum
import uuid

class EquipmentStatus(enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    MAINTENANCE = "maintenance"
    RETIRED = "retired"

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    equipment_type = Column(String(100), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(100))
    status = Column(String(50), default='available')  # Use String instead of Enum
    purchase_date = Column(Date)
    purchase_price = Column(DECIMAL(10, 2))
    current_location = Column(String(255))
    assigned_to = Column(UUID(as_uuid=True), ForeignKey('crew_members.id'))
    last_maintenance_date = Column(Date)
    next_maintenance_date = Column(Date)
    maintenance_notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    assigned_crew_member = relationship('CrewMember', backref='assigned_equipment')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'equipment_type': self.equipment_type,
            'brand': self.brand,
            'model': self.model,
            'serial_number': self.serial_number,
            'status': self.status,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'purchase_price': float(self.purchase_price) if self.purchase_price else None,
            'current_location': self.current_location,
            'assigned_to': str(self.assigned_to) if self.assigned_to else None,
            'last_maintenance_date': self.last_maintenance_date.isoformat() if self.last_maintenance_date else None,
            'next_maintenance_date': self.next_maintenance_date.isoformat() if self.next_maintenance_date else None,
            'maintenance_notes': self.maintenance_notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
