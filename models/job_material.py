"""
Job Material model for tracking materials used in jobs
"""

from sqlalchemy import Column, String, Text, DateTime, Numeric, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import db

class JobMaterial(db.Model):
    __tablename__ = 'job_materials'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey('jobs.id'), nullable=False)
    material_id = Column(UUID(as_uuid=True), ForeignKey('materials.id'), nullable=False)
    quantity_estimated = Column(Numeric(10, 2), nullable=False)
    quantity_actual = Column(Numeric(10, 2), nullable=True)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<JobMaterial {self.material.name if self.material else "Unknown"} x {self.quantity_estimated}>'
    
    @property
    def total_cost(self):
        """Calculate total cost based on estimated quantity"""
        return float(self.quantity_estimated * self.unit_cost)
    
    @property
    def actual_total_cost(self):
        """Calculate total cost based on actual quantity"""
        if self.quantity_actual:
            return float(self.quantity_actual * self.unit_cost)
        return self.total_cost
    
    @property
    def cost_variance(self):
        """Calculate cost variance between estimated and actual"""
        if self.quantity_actual:
            return self.actual_total_cost - self.total_cost
        return 0
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': str(self.id),
            'job_id': str(self.job_id),
            'material_id': str(self.material_id),
            'material_name': self.material.name if self.material else None,
            'material_type': self.material.material_type if self.material else None,
            'quantity_estimated': float(self.quantity_estimated),
            'quantity_actual': float(self.quantity_actual) if self.quantity_actual else None,
            'unit_cost': float(self.unit_cost),
            'total_cost': self.total_cost,
            'actual_total_cost': self.actual_total_cost,
            'cost_variance': self.cost_variance,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
