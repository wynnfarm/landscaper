"""
Job Crew Assignment model for tracking crew assignments to jobs
"""

from sqlalchemy import Column, String, Text, DateTime, Date, Time, Numeric, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import db

class JobCrewAssignment(db.Model):
    __tablename__ = 'job_crew_assignments'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    crew_member_id = Column(UUID(as_uuid=True), ForeignKey('crew_members.id'), nullable=False)
    role = Column(String(100), nullable=False)
    assigned_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    hours_worked = Column(Numeric(4, 2), nullable=True)
    hourly_rate = Column(Numeric(8, 2), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<JobCrewAssignment {self.crew_member.full_name if self.crew_member else "Unknown"} on {self.assigned_date}>'
    
    @property
    def total_cost(self):
        """Calculate total cost based on hours worked and hourly rate"""
        if self.hours_worked and self.hourly_rate:
            return float(self.hours_worked * self.hourly_rate)
        return 0
    
    @property
    def duration_hours(self):
        """Calculate duration in hours from start and end time"""
        if self.start_time and self.end_time:
            # Convert time to datetime for calculation
            from datetime import datetime, date
            start_datetime = datetime.combine(date.today(), self.start_time)
            end_datetime = datetime.combine(date.today(), self.end_time)
            
            # Handle overnight shifts
            if end_datetime < start_datetime:
                end_datetime = end_datetime.replace(day=end_datetime.day + 1)
            
            duration = end_datetime - start_datetime
            return duration.total_seconds() / 3600
        return None
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': str(self.id),
            'job_id': str(self.job_id),
            'job_number': self.job.job_number if self.job else None,
            'crew_member_id': str(self.crew_member_id),
            'crew_member_name': self.crew_member.full_name if self.crew_member else None,
            'role': self.role,
            'assigned_date': self.assigned_date.isoformat() if self.assigned_date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'hours_worked': float(self.hours_worked) if self.hours_worked else None,
            'duration_hours': self.duration_hours,
            'hourly_rate': float(self.hourly_rate) if self.hourly_rate else None,
            'total_cost': self.total_cost,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
