#!/usr/bin/env python3
"""
Landscaping Job Calculator System
Based on Excel analysis patterns
"""

import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

class JobCalculator:
    """Main job calculator class"""
    
    def __init__(self):
        self.job_types = {
            'pavers': PaverCalculator(),
            'walls': WallCalculator(),
            'stairs': StairCalculator(),
            'steps': StepCalculator()
        }
    
    def calculate_job(self, job_type: str, measurements: Dict) -> Dict:
        """Calculate job requirements based on type and measurements"""
        if job_type not in self.job_types:
            raise ValueError(f"Unknown job type: {job_type}")
        
        calculator = self.job_types[job_type]
        return calculator.calculate(measurements)
    
    def get_job_types(self) -> List[str]:
        """Get available job types"""
        return list(self.job_types.keys())

class PaverCalculator:
    """Paver installation calculator based on Excel patterns"""
    
    def calculate(self, measurements: Dict) -> Dict:
        """Calculate paver installation requirements"""
        
        # Extract measurements
        length_ft = measurements.get('length_ft', 0)
        length_in = measurements.get('length_in', 0)
        width_ft = measurements.get('width_ft', 0)
        width_in = measurements.get('width_in', 0)
        
        # Convert to total inches
        total_length_in = (length_ft * 12) + length_in
        total_width_in = (width_ft * 12) + width_in
        
        # Calculate area in square feet
        area_sqft = (total_length_in * total_width_in) / 144
        
        # Layer calculations based on Excel patterns
        paver_height = measurements.get('paver_height', 2.375)  # inches
        fines_depth = measurements.get('fines_depth', 2.375)     # inches
        ca11_depth = measurements.get('ca11_depth', 3.625)       # inches
        
        # Calculate total depth
        total_depth = paver_height + fines_depth + ca11_depth
        
        # Material calculations
        pavers_needed = area_sqft * (paver_height / 12)  # cubic feet
        fines_needed = area_sqft * (fines_depth / 12)     # cubic feet
        ca11_needed = area_sqft * (ca11_depth / 12)      # cubic feet
        
        # Convert to common units
        pavers_cubic_yards = pavers_needed / 27
        fines_cubic_yards = fines_needed / 27
        ca11_cubic_yards = ca11_needed / 27
        
        return {
            'job_type': 'paver_installation',
            'area_sqft': round(area_sqft, 2),
            'total_depth_inches': round(total_depth, 2),
            'materials': {
                'CA11': {
                    'quantity': round(ca11_cubic_yards, 2),
                    'unit': 'cubic yards'
                },
                'Fines': {
                    'quantity': round(fines_cubic_yards, 2),
                    'unit': 'cubic yards'
                },
                'Pavers': {
                    'quantity': round(area_sqft, 2),
                    'unit': 'square feet'
                }
            },
            'layers': [
                {'name': 'CA11 Base', 'depth': ca11_depth, 'material': 'CA11'},
                {'name': 'Fines', 'depth': fines_depth, 'material': 'Fines'},
                {'name': 'Pavers', 'depth': paver_height, 'material': 'Pavers'}
            ],
            'calculations': {
                'total_volume_cubic_yards': round((pavers_needed + fines_needed + ca11_needed) / 27, 2),
                'total_weight_tons': round((pavers_needed + fines_needed + ca11_needed) * 100 / 2000, 2)  # Approximate
            }
        }

class WallCalculator:
    """Wall construction calculator"""
    
    def calculate(self, measurements: Dict) -> Dict:
        """Calculate wall construction requirements"""
        
        # Extract measurements
        length_ft = measurements.get('length_ft', 0)
        length_in = measurements.get('length_in', 0)
        height_ft = measurements.get('height_ft', 0)
        height_in = measurements.get('height_in', 0)
        width_ft = measurements.get('width_ft', 0)
        width_in = measurements.get('width_in', 0)
        
        # Convert to total inches
        total_length_in = (length_ft * 12) + length_in
        total_height_in = (height_ft * 12) + height_in
        total_width_in = (width_ft * 12) + width_in
        
        # Calculate volume
        volume_cubic_inches = total_length_in * total_height_in * total_width_in
        volume_cubic_feet = volume_cubic_inches / 1728
        volume_cubic_yards = volume_cubic_feet / 27
        
        # Calculate surface area
        surface_area_sqft = (total_length_in * total_height_in) / 144
        
        # Material calculations
        blocks_needed = surface_area_sqft * measurements.get('blocks_per_sqft', 1.125)
        mortar_needed = volume_cubic_feet * 0.1  # 10% of volume for mortar
        
        return {
            'job_type': 'wall_construction',
            'area_sqft': round(surface_area_sqft, 2),
            'total_depth_inches': round(total_width_in, 2),
            'dimensions': {
                'length_feet': round(total_length_in / 12, 2),
                'height_feet': round(total_height_in / 12, 2),
                'width_feet': round(total_width_in / 12, 2)
            },
            'materials': {
                'Blocks': {
                    'quantity': round(blocks_needed, 0),
                    'unit': 'blocks'
                },
                'Mortar': {
                    'quantity': round(mortar_needed, 2),
                    'unit': 'cubic feet'
                },
                'Backfill': {
                    'quantity': round(volume_cubic_yards * 0.8, 2),
                    'unit': 'cubic yards'
                }
            },
            'layers': [
                {'name': 'Wall Blocks', 'depth': total_width_in, 'material': 'Blocks'}
            ],
            'calculations': {
                'total_volume_cubic_yards': round(volume_cubic_yards, 2),
                'total_weight_tons': round(volume_cubic_yards * 1.5, 2)  # Approximate
            }
        }

class StairCalculator:
    """Stair construction calculator"""
    
    def calculate(self, measurements: Dict) -> Dict:
        """Calculate stair construction requirements"""
        
        # Extract measurements
        total_rise_ft = measurements.get('total_rise_ft', 0)
        total_rise_in = measurements.get('total_rise_in', 0)
        total_run_ft = measurements.get('total_run_ft', 0)
        total_run_in = measurements.get('total_run_in', 0)
        
        # Convert to total inches
        total_rise_inches = (total_rise_ft * 12) + total_rise_in
        total_run_inches = (total_run_ft * 12) + total_run_in
        
        # Calculate number of steps
        step_count = measurements.get('step_count', 0)
        if step_count == 0:
            # Calculate optimal step count
            step_count = round(total_rise_inches / 7)  # 7 inches per step is standard
        
        # Calculate individual step dimensions
        rise_per_step = total_rise_inches / step_count
        run_per_step = total_run_inches / step_count
        
        # Material calculations
        tread_area_sqft = (run_per_step * measurements.get('tread_width', 36)) / 144
        riser_area_sqft = (rise_per_step * measurements.get('tread_width', 36)) / 144
        
        total_tread_area = tread_area_sqft * step_count
        total_riser_area = riser_area_sqft * step_count
        
        return {
            'job_type': 'stair_construction',
            'area_sqft': round(total_tread_area + total_riser_area, 2),
            'total_depth_inches': round(measurements.get('tread_width', 36), 2),
            'dimensions': {
                'total_rise_feet': round(total_rise_inches / 12, 2),
                'total_run_feet': round(total_run_inches / 12, 2),
                'step_count': step_count
            },
            'step_dimensions': {
                'rise_per_step_inches': round(rise_per_step, 2),
                'run_per_step_inches': round(run_per_step, 2)
            },
            'materials': {
                'Treads': {
                    'quantity': round(total_tread_area, 2),
                    'unit': 'square feet'
                },
                'Risers': {
                    'quantity': round(total_riser_area, 2),
                    'unit': 'square feet'
                },
                'Stringers': {
                    'quantity': 2,
                    'unit': 'pieces'
                }
            },
            'layers': [
                {'name': 'Tread Material', 'depth': run_per_step, 'material': 'Treads'},
                {'name': 'Riser Material', 'depth': rise_per_step, 'material': 'Risers'}
            ],
            'calculations': {
                'total_volume_cubic_yards': round((total_tread_area + total_riser_area) * 0.1 / 27, 2),
                'total_weight_tons': round((total_tread_area + total_riser_area) * 0.1 * 150 / 2000, 2)
            }
        }

class StepCalculator:
    """Individual step calculator"""
    
    def calculate(self, measurements: Dict) -> Dict:
        """Calculate individual step requirements"""
        
        # Extract measurements
        rise_ft = measurements.get('rise_ft', 0)
        rise_in = measurements.get('rise_in', 0)
        run_ft = measurements.get('run_ft', 0)
        run_in = measurements.get('run_in', 0)
        width_ft = measurements.get('width_ft', 0)
        width_in = measurements.get('width_in', 0)
        
        # Convert to total inches
        total_rise_inches = (rise_ft * 12) + rise_in
        total_run_inches = (run_ft * 12) + run_in
        total_width_inches = (width_ft * 12) + width_in
        
        # Calculate areas
        tread_area_sqft = (total_run_inches * total_width_inches) / 144
        riser_area_sqft = (total_rise_inches * total_width_inches) / 144
        
        # Material calculations
        tread_material = measurements.get('tread_material', 'Stone')
        riser_material = measurements.get('riser_material', 'Stone')
        
        return {
            'job_type': 'step_installation',
            'area_sqft': round(tread_area_sqft + riser_area_sqft, 2),
            'total_depth_inches': round(total_width_inches, 2),
            'dimensions': {
                'rise_inches': round(total_rise_inches, 2),
                'run_inches': round(total_run_inches, 2),
                'width_inches': round(total_width_inches, 2)
            },
            'materials': {
                'Tread Material': {
                    'quantity': round(tread_area_sqft, 2),
                    'unit': 'square feet'
                },
                'Riser Material': {
                    'quantity': round(riser_area_sqft, 2),
                    'unit': 'square feet'
                }
            },
            'layers': [
                {'name': 'Tread', 'depth': total_run_inches, 'material': 'Tread Material'},
                {'name': 'Riser', 'depth': total_rise_inches, 'material': 'Riser Material'}
            ],
            'calculations': {
                'total_volume_cubic_yards': round((tread_area_sqft + riser_area_sqft) * 0.1 / 27, 2),
                'total_weight_tons': round((tread_area_sqft + riser_area_sqft) * 0.1 * 150 / 2000, 2)
            }
        }

# Utility functions
def feet_inches_to_inches(feet: float, inches: float) -> float:
    """Convert feet and inches to total inches"""
    return (feet * 12) + inches

def inches_to_feet_inches(total_inches: float) -> Tuple[int, float]:
    """Convert total inches to feet and inches"""
    feet = int(total_inches // 12)
    inches = total_inches % 12
    return feet, inches

def format_measurement(feet: float, inches: float) -> str:
    """Format measurement as string"""
    if feet > 0:
        return f"{feet}' {inches}\""
    else:
        return f"{inches}\""

# Example usage
if __name__ == "__main__":
    calculator = JobCalculator()
    
    # Example paver calculation
    paver_measurements = {
        'length_ft': 20,
        'length_in': 6,
        'width_ft': 15,
        'width_in': 0,
        'paver_height': 2.375,
        'fines_depth': 2.375,
        'ca11_depth': 3.625
    }
    
    result = calculator.calculate_job('pavers', paver_measurements)
    print("Paver Job Calculation:")
    print(json.dumps(result, indent=2))
    
    # Example wall calculation
    wall_measurements = {
        'length_ft': 30,
        'length_in': 0,
        'height_ft': 4,
        'height_in': 0,
        'width_ft': 0,
        'width_in': 8,
        'block_type': 'Standard Concrete Block'
    }
    
    result = calculator.calculate_job('walls', wall_measurements)
    print("\nWall Job Calculation:")
    print(json.dumps(result, indent=2))
