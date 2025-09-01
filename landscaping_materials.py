"""
Landscaping Materials Database and Calculator

This module contains information about common landscaping materials used in wall construction,
including dimensions, coverage, and calculation methods for determining quantities needed.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from enum import Enum
import math


class MaterialType(Enum):
    """Types of landscaping materials."""
    RETAINING_WALL_BLOCKS = "retaining_wall_blocks"
    PAVERS = "pavers"
    STONE = "stone"
    CONCRETE = "concrete"
    BRICK = "brick"
    TIMBER = "timber"
    GABION = "gabion"


@dataclass
class MaterialSpec:
    """Specifications for a landscaping material."""
    name: str
    material_type: MaterialType
    length: float  # inches
    width: float   # inches
    height: float  # inches
    weight: float  # pounds
    coverage_per_unit: float  # square feet
    price_per_unit: float  # dollars
    description: str
    use_case: str
    installation_notes: str


class LandscapingMaterials:
    """Database of landscaping materials with calculation methods."""
    
    def __init__(self):
        self.materials = self._initialize_materials()
    
    def _initialize_materials(self) -> Dict[str, MaterialSpec]:
        """Initialize the materials database with common landscaping materials."""
        return {
            # Retaining Wall Blocks
            "versa_lok_standard": MaterialSpec(
                name="Versa-Lok Standard Block",
                material_type=MaterialType.RETAINING_WALL_BLOCKS,
                length=12.0,
                width=6.0,
                height=4.0,
                weight=35.0,
                coverage_per_unit=0.5,  # 0.5 sq ft per block
                price_per_unit=4.50,
                description="Interlocking concrete block for retaining walls",
                use_case="Retaining walls, garden walls, raised beds",
                installation_notes="Requires gravel base, interlocking design"
            ),
            
            "versa_lok_cap": MaterialSpec(
                name="Versa-Lok Cap Block",
                material_type=MaterialType.RETAINING_WALL_BLOCKS,
                length=12.0,
                width=6.0,
                height=2.0,
                weight=18.0,
                coverage_per_unit=0.5,
                price_per_unit=3.25,
                description="Cap block for finishing retaining walls",
                use_case="Top course of retaining walls",
                installation_notes="Used as final layer, provides clean finish"
            ),
            
            "allan_block_standard": MaterialSpec(
                name="Allan Block Standard",
                material_type=MaterialType.RETAINING_WALL_BLOCKS,
                length=18.0,
                width=6.0,
                height=6.0,
                weight=50.0,
                coverage_per_unit=0.75,
                price_per_unit=6.25,
                description="Large interlocking concrete block",
                use_case="Tall retaining walls, commercial applications",
                installation_notes="Heavy duty, requires equipment for installation"
            ),
            
            "keystone_standard": MaterialSpec(
                name="Keystone Standard Block",
                material_type=MaterialType.RETAINING_WALL_BLOCKS,
                length=12.0,
                width=6.0,
                height=4.0,
                weight=32.0,
                coverage_per_unit=0.5,
                price_per_unit=4.25,
                description="Versatile retaining wall block",
                use_case="Residential retaining walls, planters",
                installation_notes="Easy to install, good for DIY projects"
            ),
            
            # Pavers
            "concrete_paver_4x8": MaterialSpec(
                name="Concrete Paver 4x8",
                material_type=MaterialType.PAVERS,
                length=8.0,
                width=4.0,
                height=2.375,
                weight=8.0,
                coverage_per_unit=0.22,
                price_per_unit=1.25,
                description="Standard concrete paver",
                use_case="Patios, walkways, edging",
                installation_notes="Requires sand base, good for flat surfaces"
            ),
            
            "concrete_paver_6x6": MaterialSpec(
                name="Concrete Paver 6x6",
                material_type=MaterialType.PAVERS,
                length=6.0,
                width=6.0,
                height=2.375,
                weight=9.0,
                coverage_per_unit=0.25,
                price_per_unit=1.50,
                description="Square concrete paver",
                use_case="Patios, decorative patterns",
                installation_notes="Versatile for various patterns"
            ),
            
            # Natural Stone
            "fieldstone_irregular": MaterialSpec(
                name="Fieldstone (Irregular)",
                material_type=MaterialType.STONE,
                length=12.0,  # average
                width=8.0,    # average
                height=6.0,   # average
                weight=45.0,
                coverage_per_unit=0.67,
                price_per_unit=8.50,
                description="Natural irregular stone",
                use_case="Natural looking walls, garden features",
                installation_notes="Requires skilled mason, irregular sizing"
            ),
            
            "limestone_block": MaterialSpec(
                name="Limestone Block",
                material_type=MaterialType.STONE,
                length=12.0,
                width=6.0,
                height=4.0,
                weight=40.0,
                coverage_per_unit=0.5,
                price_per_unit=12.00,
                description="Cut limestone blocks",
                use_case="Premium walls, formal gardens",
                installation_notes="Professional installation recommended"
            ),
            
            # Concrete
            "concrete_block_8x8x16": MaterialSpec(
                name="Concrete Block 8x8x16",
                material_type=MaterialType.CONCRETE,
                length=16.0,
                width=8.0,
                height=8.0,
                weight=35.0,
                coverage_per_unit=0.89,
                price_per_unit=2.50,
                description="Standard concrete block",
                use_case="Foundation walls, structural walls",
                installation_notes="Requires mortar, professional installation"
            ),
            
            # Brick
            "standard_brick": MaterialSpec(
                name="Standard Brick",
                material_type=MaterialType.BRICK,
                length=8.0,
                width=3.625,
                height=2.25,
                weight=4.5,
                coverage_per_unit=0.2,
                price_per_unit=0.75,
                description="Standard clay brick",
                use_case="Decorative walls, planters",
                installation_notes="Requires mortar, good for small projects"
            ),
            
            # Timber
            "landscape_timber_6x6": MaterialSpec(
                name="Landscape Timber 6x6",
                material_type=MaterialType.TIMBER,
                length=96.0,  # 8 feet
                width=6.0,
                height=6.0,
                weight=25.0,
                coverage_per_unit=4.0,  # 4 feet of wall length
                price_per_unit=15.00,
                description="Pressure treated landscape timber",
                use_case="Garden walls, raised beds",
                installation_notes="Requires rebar, good for low walls"
            ),
            
            # Gabion
            "gabion_basket_3x3x6": MaterialSpec(
                name="Gabion Basket 3x3x6",
                material_type=MaterialType.GABION,
                length=72.0,  # 6 feet
                width=36.0,   # 3 feet
                height=36.0,  # 3 feet
                weight=0.0,   # empty basket
                coverage_per_unit=18.0,  # 18 sq ft face
                price_per_unit=45.00,
                description="Wire basket for stone fill",
                use_case="Large retaining walls, erosion control",
                installation_notes="Fill with local stone, requires heavy equipment"
            )
        }
    
    def get_material(self, material_id: str) -> MaterialSpec:
        """Get a specific material by ID."""
        return self.materials.get(material_id)
    
    def get_materials_by_type(self, material_type: MaterialType) -> List[MaterialSpec]:
        """Get all materials of a specific type."""
        return [mat for mat in self.materials.values() if mat.material_type == material_type]
    
    def get_all_materials(self) -> List[MaterialSpec]:
        """Get all available materials."""
        return list(self.materials.values())
    
    def calculate_wall_materials(self, 
                                wall_length: float,  # feet
                                wall_height: float,  # feet
                                material_id: str,
                                include_base: bool = True,
                                include_cap: bool = True) -> Dict[str, Any]:
        """
        Calculate materials needed for a landscape wall.
        
        Args:
            wall_length: Length of wall in feet
            wall_height: Height of wall in feet
            material_id: ID of the primary material
            include_base: Whether to include base materials
            include_cap: Whether to include cap materials
            
        Returns:
            Dictionary with material calculations
        """
        material = self.get_material(material_id)
        if not material:
            raise ValueError(f"Material {material_id} not found")
        
        # Convert wall dimensions to inches
        wall_length_inches = wall_length * 12
        wall_height_inches = wall_height * 12
        
        # Calculate materials needed
        results = {
            "wall_specifications": {
                "length_feet": wall_length,
                "height_feet": wall_height,
                "length_inches": wall_length_inches,
                "height_inches": wall_height_inches
            },
            "primary_material": {
                "name": material.name,
                "type": material.material_type.value,
                "dimensions": f"{material.length}\" x {material.width}\" x {material.height}\"",
                "weight_per_unit": material.weight,
                "price_per_unit": material.price_per_unit
            },
            "calculations": {},
            "materials_needed": {},
            "cost_breakdown": {},
            "installation_notes": []
        }
        
        # Calculate primary material quantities
        if material.material_type == MaterialType.RETAINING_WALL_BLOCKS:
            self._calculate_retaining_wall_blocks(results, material, wall_length_inches, wall_height_inches)
        elif material.material_type == MaterialType.PAVERS:
            self._calculate_paver_wall(results, material, wall_length_inches, wall_height_inches)
        elif material.material_type == MaterialType.STONE:
            self._calculate_stone_wall(results, material, wall_length_inches, wall_height_inches)
        elif material.material_type == MaterialType.CONCRETE:
            self._calculate_concrete_block_wall(results, material, wall_length_inches, wall_height_inches)
        elif material.material_type == MaterialType.BRICK:
            self._calculate_brick_wall(results, material, wall_length_inches, wall_height_inches)
        elif material.material_type == MaterialType.TIMBER:
            self._calculate_timber_wall(results, material, wall_length_inches, wall_height_inches)
        elif material.material_type == MaterialType.GABION:
            self._calculate_gabion_wall(results, material, wall_length_inches, wall_height_inches)
        
        # Add base materials if requested
        if include_base:
            self._add_base_materials(results, wall_length, wall_height)
        
        # Add cap materials if requested
        if include_cap and material.material_type == MaterialType.RETAINING_WALL_BLOCKS:
            self._add_cap_materials(results, wall_length_inches)
        
        # Calculate total costs
        self._calculate_total_costs(results)
        
        # Add installation notes
        results["installation_notes"].extend([
            material.installation_notes,
            f"Wall area: {wall_length * wall_height:.1f} square feet",
            f"Estimated installation time: {self._estimate_installation_time(results)} hours"
        ])
        
        return results
    
    def _calculate_retaining_wall_blocks(self, results: Dict, material: MaterialSpec, 
                                       wall_length_inches: float, wall_height_inches: float):
        """Calculate quantities for retaining wall blocks."""
        # Calculate blocks per course
        blocks_per_course = math.ceil(wall_length_inches / material.length)
        
        # Calculate number of courses
        courses = math.ceil(wall_height_inches / material.height)
        
        # Total blocks needed
        total_blocks = blocks_per_course * courses
        
        results["calculations"] = {
            "blocks_per_course": blocks_per_course,
            "number_of_courses": courses,
            "total_blocks": total_blocks
        }
        
        results["materials_needed"] = {
            "primary_blocks": total_blocks,
            "gravel_base_cubic_yards": round(wall_length_inches * material.width * 6 / 46656, 2),  # 6" base
            "sand_bed_cubic_yards": round(wall_length_inches * material.width * 2 / 46656, 2)     # 2" sand
        }
    
    def _calculate_paver_wall(self, results: Dict, material: MaterialSpec,
                            wall_length_inches: float, wall_height_inches: float):
        """Calculate quantities for paver walls."""
        # Pavers are typically used for low walls (2-3 courses max)
        courses = min(math.ceil(wall_height_inches / material.height), 3)
        pavers_per_course = math.ceil(wall_length_inches / material.length)
        total_pavers = pavers_per_course * courses
        
        results["calculations"] = {
            "pavers_per_course": pavers_per_course,
            "number_of_courses": courses,
            "total_pavers": total_pavers
        }
        
        results["materials_needed"] = {
            "pavers": total_pavers,
            "sand_base_cubic_yards": round(wall_length_inches * material.width * 4 / 46656, 2),
            "paver_sand_cubic_yards": round(wall_length_inches * material.width * 1 / 46656, 2)
        }
    
    def _calculate_stone_wall(self, results: Dict, material: MaterialSpec,
                            wall_length_inches: float, wall_height_inches: float):
        """Calculate quantities for stone walls."""
        # Stone walls are irregular, estimate based on coverage
        wall_area_sq_ft = (wall_length_inches * wall_height_inches) / 144
        stones_needed = math.ceil(wall_area_sq_ft / material.coverage_per_unit)
        
        results["calculations"] = {
            "wall_area_square_feet": round(wall_area_sq_ft, 2),
            "estimated_stones": stones_needed
        }
        
        results["materials_needed"] = {
            "stone_blocks": stones_needed,
            "mortar_bags": math.ceil(stones_needed * 0.1),  # Estimate
            "gravel_base_cubic_yards": round(wall_length_inches * 12 * 6 / 46656, 2)
        }
    
    def _calculate_concrete_block_wall(self, results: Dict, material: MaterialSpec,
                                     wall_length_inches: float, wall_height_inches: float):
        """Calculate quantities for concrete block walls."""
        blocks_per_course = math.ceil(wall_length_inches / material.length)
        courses = math.ceil(wall_height_inches / material.height)
        total_blocks = blocks_per_course * courses
        
        results["calculations"] = {
            "blocks_per_course": blocks_per_course,
            "number_of_courses": courses,
            "total_blocks": total_blocks
        }
        
        results["materials_needed"] = {
            "concrete_blocks": total_blocks,
            "mortar_bags": math.ceil(total_blocks * 0.3),
            "rebar_pieces": math.ceil(wall_length_inches / 48),  # Every 4 feet
            "concrete_footings_cubic_yards": round(wall_length_inches * 12 * 8 / 46656, 2)
        }
    
    def _calculate_brick_wall(self, results: Dict, material: MaterialSpec,
                            wall_length_inches: float, wall_height_inches: float):
        """Calculate quantities for brick walls."""
        # Standard brick wall with mortar joints
        bricks_per_course = math.ceil(wall_length_inches / (material.length + 0.375))  # + mortar
        courses = math.ceil(wall_height_inches / (material.height + 0.375))  # + mortar
        total_bricks = bricks_per_course * courses
        
        results["calculations"] = {
            "bricks_per_course": bricks_per_course,
            "number_of_courses": courses,
            "total_bricks": total_bricks
        }
        
        results["materials_needed"] = {
            "bricks": total_bricks,
            "mortar_bags": math.ceil(total_bricks * 0.05),
            "sand_cubic_yards": round(total_bricks * 0.001, 2)
        }
    
    def _calculate_timber_wall(self, results: Dict, material: MaterialSpec,
                             wall_length_inches: float, wall_height_inches: float):
        """Calculate quantities for timber walls."""
        # Timber walls are typically 6" high per course
        courses = math.ceil(wall_height_inches / material.height)
        timbers_needed = math.ceil(wall_length_inches / material.length) * courses
        
        results["calculations"] = {
            "timbers_per_course": math.ceil(wall_length_inches / material.length),
            "number_of_courses": courses,
            "total_timbers": timbers_needed
        }
        
        results["materials_needed"] = {
            "landscape_timbers": timbers_needed,
            "rebar_pieces": timbers_needed * 2,  # 2 per timber
            "gravel_base_cubic_yards": round(wall_length_inches * 6 * 4 / 46656, 2)
        }
    
    def _calculate_gabion_wall(self, results: Dict, material: MaterialSpec,
                             wall_length_inches: float, wall_height_inches: float):
        """Calculate quantities for gabion walls."""
        # Gabion baskets are typically 3' x 3' x 6'
        baskets_length = math.ceil(wall_length_inches / material.length)
        baskets_height = math.ceil(wall_height_inches / material.height)
        total_baskets = baskets_length * baskets_height
        
        # Stone fill (typically 1.5 tons per cubic yard)
        stone_cubic_yards = total_baskets * (material.length * material.width * material.height) / 46656
        
        results["calculations"] = {
            "baskets_length": baskets_length,
            "baskets_height": baskets_height,
            "total_baskets": total_baskets,
            "stone_cubic_yards": round(stone_cubic_yards, 2)
        }
        
        results["materials_needed"] = {
            "gabion_baskets": total_baskets,
            "stone_fill_tons": round(stone_cubic_yards * 1.5, 1),
            "geotextile_square_feet": round(wall_length_inches * 12 / 144, 0)
        }
    
    def _add_base_materials(self, results: Dict, wall_length: float, wall_height: float):
        """Add base materials to the calculation."""
        if "materials_needed" not in results:
            results["materials_needed"] = {}
        
        # Add common base materials
        results["materials_needed"].update({
            "landscape_fabric_square_feet": round(wall_length * 2, 0),  # 2' wide strip
            "drainage_pipe_feet": round(wall_length, 0) if wall_height > 3 else 0
        })
    
    def _add_cap_materials(self, results: Dict, wall_length_inches: float):
        """Add cap materials for retaining wall blocks."""
        # Find cap block material
        cap_material = None
        for material in self.materials.values():
            if "cap" in material.name.lower():
                cap_material = material
                break
        
        if cap_material:
            cap_blocks = math.ceil(wall_length_inches / cap_material.length)
            results["materials_needed"]["cap_blocks"] = cap_blocks
            results["cost_breakdown"]["cap_blocks"] = cap_blocks * cap_material.price_per_unit
    
    def _calculate_total_costs(self, results: Dict):
        """Calculate total material costs."""
        total_cost = 0
        cost_breakdown = {}
        
        material = self.get_material(results["primary_material"]["name"].lower().replace(" ", "_").replace("-", "_"))
        if material:
            primary_quantity = results["materials_needed"].get("primary_blocks", 
                                                           results["materials_needed"].get("pavers", 
                                                           results["materials_needed"].get("stone_blocks",
                                                           results["materials_needed"].get("concrete_blocks",
                                                           results["materials_needed"].get("bricks",
                                                           results["materials_needed"].get("landscape_timbers",
                                                           results["materials_needed"].get("gabion_baskets", 0)))))))
            
            primary_cost = primary_quantity * material.price_per_unit
            cost_breakdown["primary_material"] = primary_cost
            total_cost += primary_cost
        
        # Add other material costs (estimates)
        cost_estimates = {
            "gravel_base_cubic_yards": 25.00,
            "sand_bed_cubic_yards": 30.00,
            "mortar_bags": 8.00,
            "rebar_pieces": 5.00,
            "landscape_fabric_square_feet": 0.50,
            "drainage_pipe_feet": 3.00,
            "stone_fill_tons": 35.00,
            "geotextile_square_feet": 2.00
        }
        
        for material_name, quantity in results["materials_needed"].items():
            if material_name in cost_estimates:
                cost = quantity * cost_estimates[material_name]
                cost_breakdown[material_name] = cost
                total_cost += cost
        
        results["cost_breakdown"] = cost_breakdown
        results["total_estimated_cost"] = round(total_cost, 2)
    
    def _estimate_installation_time(self, results: Dict) -> int:
        """Estimate installation time in hours."""
        wall_area = results["wall_specifications"]["length_feet"] * results["wall_specifications"]["height_feet"]
        
        # Base time estimates (hours per 100 sq ft)
        time_per_100_sqft = {
            "retaining_wall_blocks": 8,
            "pavers": 12,
            "stone": 20,
            "concrete": 15,
            "brick": 18,
            "timber": 6,
            "gabion": 4
        }
        
        material_type = results["primary_material"]["type"]
        base_time = time_per_100_sqft.get(material_type, 10)
        
        return max(1, round((wall_area / 100) * base_time))


# Example usage and testing
if __name__ == "__main__":
    materials = LandscapingMaterials()
    
    # Example calculation for a 20' x 4' retaining wall
    result = materials.calculate_wall_materials(
        wall_length=20.0,
        wall_height=4.0,
        material_id="versa_lok_standard",
        include_base=True,
        include_cap=True
    )
    
    print("Landscape Wall Material Calculator")
    print("=" * 50)
    print(f"Wall: {result['wall_specifications']['length_feet']}' x {result['wall_specifications']['height_feet']}'")
    print(f"Material: {result['primary_material']['name']}")
    print(f"Total Estimated Cost: ${result['total_estimated_cost']}")
    print("\nMaterials Needed:")
    for material, quantity in result['materials_needed'].items():
        print(f"  {material}: {quantity}")
