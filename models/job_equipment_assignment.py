"""
Job Equipment Assignment model for tracking equipment assignments to jobs
"""

from sqlalchemy import Column, String, Text, DateTime, Date, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import db

class JobEquipmentAssignment(db.Model):
    __tablename__ = 'job_equipment_assignments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    equipment_id = Column(UUID(as_uuid=True), ForeignKey('equipment.id'), nullable=False)
    assigned_date = Column(Date, nullable=False)
    returned_date = Column(Date, nullable=True)
    condition_on_assignment = Column(Text, nullable=True)
    condition_on_return = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<JobEquipmentAssignment {self.equipment.name if self.equipment else "Unknown"} on {self.assigned_date}>'
    
    @property
    def is_returned(self):
        """Check if equipment has been returned"""
        return self.returned_date is not None
    
    @property
    def assignment_duration_days(self):
        """Calculate assignment duration in days"""
        if self.returned_date:
            return (self.returned_date - self.assigned_date).days + 1
        else:
            from datetime import date
            return (date.today() - self.assigned_date).days + 1
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': str(self.id),
            'job_id': str(self.job_id),
            'job_number': self.job.job_number if self.job else None,
            'equipment_id': str(self.equipment_id),
            'equipment_name': self.equipment.name if self.equipment else None,
            'equipment_type': self.equipment.equipment_type if self.equipment else None,
            'assigned_date': self.assigned_date.isoformat() if self.assigned_date else None,
            'returned_date': self.returned_date.isoformat() if self.returned_date else None,
            'is_returned': self.is_returned,
            'assignment_duration_days': self.assignment_duration_days,
            'condition_on_assignment': self.condition_on_assignment,
            'condition_on_return': self.condition_on_return,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
