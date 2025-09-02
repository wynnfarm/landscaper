"""
Job Time Entry model for tracking time worked on jobs
"""

from sqlalchemy import Column, String, Text, DateTime, Date, Time, Numeric, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import db

class JobTimeEntry(db.Model):
    __tablename__ = 'job_time_entries'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    crew_member_id = Column(UUID(as_uuid=True), ForeignKey('crew_members.id'), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=True)
    break_duration_minutes = Column(Numeric(4, 0), default=0)
    activity_description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<JobTimeEntry {self.crew_member.full_name if self.crew_member else "Unknown"} on {self.date}>'
    
    @property
    def total_hours(self):
        """Calculate total hours worked"""
        if self.end_time:
            # Convert time to datetime for calculation
            from datetime import datetime, date
            start_datetime = datetime.combine(date.today(), self.start_time)
            end_datetime = datetime.combine(date.today(), self.end_time)
            
            # Handle overnight shifts
            if end_datetime < start_datetime:
                end_datetime = end_datetime.replace(day=end_datetime.day + 1)
            
            duration = end_datetime - start_datetime
            total_minutes = duration.total_seconds() / 60
            break_minutes = float(self.break_duration_minutes) if self.break_duration_minutes else 0
            return (total_minutes - break_minutes) / 60
        return 0
    
    @property
    def is_complete(self):
        """Check if time entry is complete (has end time)"""
        return self.end_time is not None
    
    @property
    def duration_text(self):
        """Get duration as formatted text"""
        hours = self.total_hours
        if hours < 1:
            minutes = int(hours * 60)
            return f"{minutes} minutes"
        else:
            whole_hours = int(hours)
            minutes = int((hours - whole_hours) * 60)
            if minutes > 0:
                return f"{whole_hours}h {minutes}m"
            else:
                return f"{whole_hours} hours"
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': str(self.id),
            'job_id': str(self.job_id),
            'job_number': self.job.job_number if self.job else None,
            'crew_member_id': str(self.crew_member_id),
            'crew_member_name': self.crew_member.full_name if self.crew_member else None,
            'date': self.date.isoformat() if self.date else None,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'break_duration_minutes': float(self.break_duration_minutes) if self.break_duration_minutes else 0,
            'total_hours': self.total_hours,
            'duration_text': self.duration_text,
            'activity_description': self.activity_description,
            'is_complete': self.is_complete,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
