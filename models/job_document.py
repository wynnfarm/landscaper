"""
Job Document model for tracking photos and documents related to jobs
"""

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import db

class JobDocument(db.Model):
    __tablename__ = 'job_documents'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=True)
    document_type = Column(String(100), nullable=True)  # before_photo, after_photo, progress_photo, invoice, permit, other
    description = Column(Text, nullable=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('crew_members.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f'<JobDocument {self.file_name} ({self.document_type})>'
    
    @property
    def formatted_file_size(self):
        """Get formatted file size"""
        if self.file_size:
            if self.file_size < 1024:
                return f"{self.file_size} B"
            elif self.file_size < 1024 * 1024:
                return f"{self.file_size / 1024:.1f} KB"
            else:
                return f"{self.file_size / (1024 * 1024):.1f} MB"
        return None
    
    @property
    def document_type_text(self):
        """Get document type as formatted text"""
        type_map = {
            'before_photo': 'Before Photo',
            'after_photo': 'After Photo',
            'progress_photo': 'Progress Photo',
            'invoice': 'Invoice',
            'permit': 'Permit',
            'other': 'Other'
        }
        return type_map.get(self.document_type, self.document_type.title() if self.document_type else 'Unknown')
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': str(self.id),
            'job_id': str(self.job_id),
            'job_number': self.job.job_number if self.job else None,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'formatted_file_size': self.formatted_file_size,
            'document_type': self.document_type,
            'document_type_text': self.document_type_text,
            'description': self.description,
            'uploaded_by': str(self.uploaded_by) if self.uploaded_by else None,
            'uploader_name': self.uploader.full_name if self.uploader else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
