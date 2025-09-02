"""
Job model for landscaping projects
"""

from sqlalchemy import Column, String, Text, DECIMAL, Boolean, DateTime, Date, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import db
import enum
import uuid

class JobStatus(enum.Enum):
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Job(db.Model):
    __tablename__ = 'jobs'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_number = Column(String(50), unique=True, nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey('clients.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    job_type = Column(String(100), nullable=False)
    status = Column(String(50), default='planning')  # Use String instead of Enum
    priority = Column(Integer, default=3)
    
    # Location information
    site_address_line1 = Column(String(255))
    site_address_line2 = Column(String(255))
    site_city = Column(String(100))
    site_state = Column(String(50))
    site_postal_code = Column(String(20))
    site_notes = Column(Text)
    
    # Scheduling
    estimated_start_date = Column(Date)
    estimated_end_date = Column(Date)
    actual_start_date = Column(Date)
    actual_end_date = Column(Date)
    
    # Financial
    estimated_cost = Column(DECIMAL(12, 2))
    actual_cost = Column(DECIMAL(12, 2))
    labor_hours_estimated = Column(DECIMAL(8, 2))
    labor_hours_actual = Column(DECIMAL(8, 2))
    
    # Project management
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey('crew_members.id'))
    lead_worker_id = Column(UUID(as_uuid=True), ForeignKey('crew_members.id'))
    
    # Additional fields
    weather_dependent = Column(Boolean, default=False)
    requires_permits = Column(Boolean, default=False)
    permit_numbers = Column(Text)
    special_instructions = Column(Text)
    completion_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True), ForeignKey('crew_members.id'))
    
    # Relationships
    client = relationship('Client', backref='jobs')
    supervisor = relationship('CrewMember', foreign_keys=[supervisor_id], backref='supervised_jobs')
    lead_worker = relationship('CrewMember', foreign_keys=[lead_worker_id], backref='led_jobs')
    creator = relationship('CrewMember', foreign_keys=[created_by], backref='created_jobs')
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': str(self.id),
            'job_number': self.job_number,
            'client_id': str(self.client_id),
            'title': self.title,
            'description': self.description,
            'job_type': self.job_type,
            'status': self.status,
            'priority': self.priority,
            'site_address_line1': self.site_address_line1,
            'site_address_line2': self.site_address_line2,
            'site_city': self.site_city,
            'site_state': self.site_state,
            'site_postal_code': self.site_postal_code,
            'site_notes': self.site_notes,
            'estimated_start_date': self.estimated_start_date.isoformat() if self.estimated_start_date else None,
            'estimated_end_date': self.estimated_end_date.isoformat() if self.estimated_end_date else None,
            'actual_start_date': self.actual_start_date.isoformat() if self.actual_start_date else None,
            'actual_end_date': self.actual_end_date.isoformat() if self.actual_end_date else None,
            'estimated_cost': float(self.estimated_cost) if self.estimated_cost else None,
            'actual_cost': float(self.actual_cost) if self.actual_cost else None,
            'labor_hours_estimated': float(self.labor_hours_estimated) if self.labor_hours_estimated else None,
            'labor_hours_actual': float(self.labor_hours_actual) if self.labor_hours_actual else None,
            'supervisor_id': str(self.supervisor_id) if self.supervisor_id else None,
            'lead_worker_id': str(self.lead_worker_id) if self.lead_worker_id else None,
            'weather_dependent': self.weather_dependent,
            'requires_permits': self.requires_permits,
            'permit_numbers': self.permit_numbers,
            'special_instructions': self.special_instructions,
            'completion_notes': self.completion_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': str(self.created_by) if self.created_by else None
        }
