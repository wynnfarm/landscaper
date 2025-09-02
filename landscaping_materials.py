"""
Landscaping Materials Database and Calculator

This module contains information about common landscaping materials used in wall construction,
including dimensions, coverage, and calculation methods for determining quantities needed.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple
from enum import Enum
import math
import logging

# Setup logging
logger = logging.getLogger(__name__)


class MaterialType(Enum):
    """Types of landscaping materials."""
    RETAINING_WALL_BLOCKS = "retaining_wall_blocks"
    PAVERS = "pavers"
    STONE = "stone"
    CONCRETE = "concrete"
    BRICK = "brick"
    TIMBER = "timber"
    GABION = "gabion"
    BLOCK = "block"
    WOOD = "wood"
    METAL = "metal"
    OTHER = "other"


@dataclass
class MaterialSpec:
    """Specifications for a landscaping material."""
    id: str
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
        self.materials = {}  # Will be populated on-demand
        self._materials_loaded = False
    
    def _load_materials_from_database(self):
        """Load materials from the database and convert to MaterialSpec objects."""
        try:
            from flask import current_app
            from models.material import Material
            
            # Check if we're in a Flask app context
            if current_app:
                db_materials = Material.query.filter_by(is_active=True).all()
                logger.info(f"Loading {len(db_materials)} materials from database")
                
                for db_material in db_materials:
                    # Convert database material to MaterialSpec
                    material_spec = self._convert_db_material_to_spec(db_material)
                    if material_spec:
                        self.materials[str(db_material.id)] = material_spec
                        logger.info(f"Loaded material: {db_material.name} (ID: {db_material.id})")
                    else:
                        logger.warning(f"Failed to convert material: {db_material.name} (ID: {db_material.id})")
                        
                logger.info(f"Total materials loaded: {len(self.materials)}")
            else:
                logger.warning("No Flask app context available, using fallback materials")
                self.materials = self._initialize_fallback_materials()
                    
        except Exception as e:
            logger.error(f"Error loading materials from database: {e}")
            # Fallback to hardcoded materials if database fails
            self.materials = self._initialize_fallback_materials()
    
    def _convert_db_material_to_spec(self, db_material) -> MaterialSpec:
        """Convert a database Material to a MaterialSpec."""
        try:
            # Map database material_type to our enum
            material_type_map = {
                'concrete': MaterialType.CONCRETE,
                'stone': MaterialType.STONE,
                'brick': MaterialType.BRICK,
                'block': MaterialType.BLOCK,
                'wood': MaterialType.WOOD,
                'metal': MaterialType.METAL,
                'other': MaterialType.OTHER
            }
            
            material_type = material_type_map.get(db_material.material_type, MaterialType.OTHER)
            
            # Calculate coverage per unit based on dimensions
            length = float(db_material.length_inches) if db_material.length_inches else 0
            width = float(db_material.width_inches) if db_material.width_inches else 0
            height = float(db_material.height_inches) if db_material.height_inches else 0
            
            # For wall materials, coverage is length * height
            coverage_per_unit = (length * height) / 144.0 if length and height else 0.5
            
            return MaterialSpec(
                id=db_material.id,
                name=db_material.name,
                material_type=material_type,
                length=length,
                width=width,
                height=height,
                weight=db_material.weight_lbs or 0,
                coverage_per_unit=coverage_per_unit,
                price_per_unit=db_material.price_per_unit or 0,
                description=db_material.description or "",
                use_case=db_material.use_case or "",
                installation_notes=db_material.installation_notes or ""
            )
        except Exception as e:
            logger.error(f"Error converting material {db_material.id}: {e}")
            return None
    
    def _initialize_fallback_materials(self) -> Dict[str, MaterialSpec]:
        """Initialize fallback materials if database fails."""
        return {
            # Concrete Block
            "concrete_block": MaterialSpec(
                id="concrete_block",
                name="Concrete Block",
                material_type=MaterialType.CONCRETE,
                length=16.0,
                width=8.0,
                height=8.0,
                weight=35.0,
                coverage_per_unit=0.89,  # 16" x 8" = 0.89 sq ft
                price_per_unit=2.50,
                description="Standard concrete block for retaining walls",
                use_case="Retaining walls, garden walls",
                installation_notes="Requires mortar between blocks, ensure proper drainage"
            ),
            
            # Natural Stone
            "natural_stone": MaterialSpec(
                id="natural_stone",
                name="Natural Stone",
                material_type=MaterialType.STONE,
                length=12.0,
                width=6.0,
                height=2.0,
                weight=15.0,
                coverage_per_unit=0.5,  # 12" x 2" = 0.5 sq ft
                price_per_unit=8.75,
                description="Natural stone for decorative walls",
                use_case="Decorative walls, facades",
                installation_notes="Apply with construction adhesive, seal after installation"
            ),
            
            # Brick
            "brick": MaterialSpec(
                id="brick",
                name="Red Clay Brick",
                material_type=MaterialType.BRICK,
                length=8.0,
                width=4.0,
                height=2.25,
                weight=4.5,
                coverage_per_unit=0.125,  # 8" x 2.25" = 0.125 sq ft
                price_per_unit=0.85,
                description="Traditional red clay brick",
                use_case="Garden walls, walkways",
                installation_notes="Use mortar joints, consider weather sealing"
            )
        }
    
    def _ensure_materials_loaded(self):
        """Ensure materials are loaded from database."""
        if not self._materials_loaded:
            self._load_materials_from_database()
            self._materials_loaded = True
    
    def get_material(self, material_id: str) -> MaterialSpec:
        """Get a specific material by ID."""
        self._ensure_materials_loaded()
        logger.info(f"Looking for material with ID: {material_id}")
        logger.info(f"Available material IDs: {list(self.materials.keys())}")
        # Convert material_id to string for comparison
        material_id_str = str(material_id)
        return self.materials.get(material_id_str)
    
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
        try:
            material = self.get_material(material_id)
            if not material:
                raise ValueError(f"Material {material_id} not found")
            
            # Convert wall dimensions to inches
            wall_length_inches = wall_length * 12
            wall_height_inches = wall_height * 12
            
            logger.info(f"Starting calculation for wall: {wall_length}' x {wall_height}'")
            
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
        
            # Calculate primary material quantities based on material type
            if material.material_type in [MaterialType.CONCRETE, MaterialType.BLOCK]:
                self._calculate_concrete_block_wall(results, material, wall_length_inches, wall_height_inches)
            elif material.material_type == MaterialType.STONE:
                self._calculate_stone_wall(results, material, wall_length_inches, wall_height_inches)
            elif material.material_type == MaterialType.BRICK:
                self._calculate_brick_wall(results, material, wall_length_inches, wall_height_inches)
            elif material.material_type == MaterialType.WOOD:
                self._calculate_timber_wall(results, material, wall_length_inches, wall_height_inches)
            else:
                # Default to concrete block calculation for unknown types
                self._calculate_concrete_block_wall(results, material, wall_length_inches, wall_height_inches)
            
            # Add base materials if requested
            if include_base:
                self._add_base_materials(results, wall_length, wall_height)
            
            # Add cap materials if requested
            if include_cap and material.material_type in [MaterialType.CONCRETE, MaterialType.BLOCK]:
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
        except Exception as e:
            logger.error(f"Error in calculate_wall_materials: {e}")
            raise
    
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
        # Check for valid dimensions and use defaults if needed
        length = material.length if material.length else 16.0
        height = material.height if material.height else 8.0
        width = material.width if material.width else 8.0
        
        logger.info(f"Calculating concrete block wall with dimensions: length={length}, height={height}, width={width}")
        logger.info(f"Wall dimensions: {wall_length_inches} x {wall_height_inches} inches")
        
        blocks_per_course = math.ceil(wall_length_inches / length)
        courses = math.ceil(wall_height_inches / height)
        total_blocks = blocks_per_course * courses
        
        logger.info(f"Concrete block calculation: blocks_per_course={blocks_per_course}, courses={courses}, total_blocks={total_blocks}")
        
        results["calculations"] = {
            "blocks_per_course": blocks_per_course,
            "number_of_courses": courses,
            "total_blocks": total_blocks
        }
        
        # Calculate materials needed with logging
        mortar_bags = math.ceil(total_blocks * 0.3)
        rebar_pieces = math.ceil(wall_length_inches / 48)  # Every 4 feet
        concrete_footings = round(wall_length_inches * 12 * 8 / 46656, 2)
        
        logger.info(f"Materials calculation: mortar_bags={mortar_bags}, rebar_pieces={rebar_pieces}, concrete_footings={concrete_footings}")
        
        results["materials_needed"] = {
            "concrete_blocks": total_blocks,
            "mortar_bags": mortar_bags,
            "rebar_pieces": rebar_pieces,
            "concrete_footings_cubic_yards": concrete_footings
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
        
        if cap_material and cap_material.length and cap_material.length > 0:
            cap_blocks = math.ceil(wall_length_inches / cap_material.length)
            results["materials_needed"]["cap_blocks"] = cap_blocks
            if "cost_breakdown" not in results:
                results["cost_breakdown"] = {}
            results["cost_breakdown"]["cap_blocks"] = cap_blocks * cap_material.price_per_unit
            logger.info(f"Added cap materials: {cap_blocks} cap blocks")
        else:
            logger.info("No suitable cap material found, skipping cap materials")
    
    def _calculate_total_costs(self, results: Dict):
        """Calculate total material costs."""
        logger.info("Starting total cost calculation")
        total_cost = 0
        cost_breakdown = {}
        
        # Get the primary material from the results
        primary_material_name = results["primary_material"]["name"]
        logger.info(f"Primary material: {primary_material_name}")
        
        # Find the material in our database
        primary_material = None
        for material in self.materials.values():
            if material.name == primary_material_name:
                primary_material = material
                break
        
        logger.info(f"Found primary material: {primary_material.name if primary_material else 'None'}")
        
        if primary_material:
            # Get the primary quantity based on material type
            primary_quantity = 0
            if primary_material.material_type in [MaterialType.CONCRETE, MaterialType.BLOCK]:
                primary_quantity = results["materials_needed"].get("concrete_blocks", 0)
            elif primary_material.material_type == MaterialType.STONE:
                primary_quantity = results["materials_needed"].get("stone_blocks", 0)
            elif primary_material.material_type == MaterialType.BRICK:
                primary_quantity = results["materials_needed"].get("bricks", 0)
            elif primary_material.material_type == MaterialType.WOOD:
                primary_quantity = results["materials_needed"].get("landscape_timbers", 0)
            else:
                # Default to first material in the list
                primary_quantity = next(iter(results["materials_needed"].values()), 0)
            
            logger.info(f"Primary quantity: {primary_quantity}")
            
            # Check for zero quantity
            if primary_quantity <= 0:
                logger.warning(f"Primary quantity is {primary_quantity}, using minimum value of 1")
                primary_quantity = 1
            
            logger.info(f"Calculating primary cost: {primary_quantity} * {primary_material.price_per_unit}")
            primary_cost = float(primary_quantity * primary_material.price_per_unit)
            cost_breakdown["primary_material"] = round(primary_cost, 2)
            total_cost += primary_cost
            logger.info(f"Primary cost: ${primary_cost}")
        
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
        
        logger.info("Calculating additional material costs")
        for material_name, quantity in results["materials_needed"].items():
            if material_name in cost_estimates:
                cost = quantity * cost_estimates[material_name]
                cost_breakdown[material_name] = cost
                total_cost += cost
                logger.info(f"Additional cost for {material_name}: {quantity} * ${cost_estimates[material_name]} = ${cost}")
        
        results["cost_breakdown"] = cost_breakdown
        results["total_estimated_cost"] = round(total_cost, 2)
        logger.info(f"Total estimated cost: ${total_cost}")
    
    def _estimate_installation_time(self, results: Dict) -> int:
        """Estimate installation time in hours."""
        wall_area = results["wall_specifications"]["length_feet"] * results["wall_specifications"]["height_feet"]
        
        logger.info(f"Estimating installation time for wall area: {wall_area} sq ft")
        
        # Check for zero wall area
        if wall_area <= 0:
            logger.warning(f"Wall area is {wall_area}, using minimum value of 1")
            wall_area = 1.0
        
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
        
        estimated_time = max(1, round((wall_area / 100) * base_time))
        logger.info(f"Estimated installation time: {estimated_time} hours")
        
        return estimated_time


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


