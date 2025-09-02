"""
Crew member model for landscaping staff
"""

from sqlalchemy import Column, String, Text, DECIMAL, Boolean, DateTime, Date, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .base import db
import enum
import uuid

class CrewRole(enum.Enum):
    SUPERVISOR = "supervisor"
    LEAD = "lead"
    OPERATOR = "operator"
    LABORER = "laborer"
    SPECIALIST = "specialist"

class CrewMember(db.Model):
    __tablename__ = 'crew_members'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True)
    phone = Column(String(20))
    role = Column(String(50), nullable=False)  # Use String instead of Enum
    hire_date = Column(Date)
    hourly_rate = Column(DECIMAL(8, 2))
    is_active = Column(Boolean, default=True)
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'is_active': self.is_active,
            'emergency_contact_name': self.emergency_contact_name,
            'emergency_contact_phone': self.emergency_contact_phone,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
