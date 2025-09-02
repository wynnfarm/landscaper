"""
Persona Manager MCP Client for Landscaper Project

This client integrates with the persona-manager MCP to provide intelligent
persona selection and management for the landscaper AI agent.
"""

import json
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class PersonaManagerClient:
    """Client for interacting with the Persona Manager MCP."""
    
    def __init__(self, personas_dir: Optional[str] = None):
        self.personas_dir = Path(personas_dir) if personas_dir else Path.cwd() / "personas"
        self.personas_dir.mkdir(exist_ok=True)
        self.personas_file = self.personas_dir / "landscaper_personas.json"
        
        # Initialize personas if they don't exist
        if not self.personas_file.exists():
            self._initialize_landscaper_personas()
    
    def _initialize_landscaper_personas(self):
        """Initialize landscaper-specific personas."""
        landscaper_personas = {
            "customer_service_rep": {
                "id": "customer_service_rep",
                "name": "Customer Service Representative",
                "description": "Friendly and professional customer service representative specializing in landscaping services",
                "expertise": [
                    "Customer Service",
                    "Landscaping Services",
                    "Appointment Scheduling",
                    "Problem Resolution",
                    "Service Recommendations"
                ],
                "communication_style": "Warm, professional, and helpful",
                "context": "Use for customer inquiries, service questions, appointment scheduling, and general support",
                "personality_traits": ["empathetic", "patient", "solution-oriented", "professional"],
                "task_categories": ["customer_service", "business"],
                "audience": "customers",
                "output_format": "conversational",
                "created_at": datetime.now().isoformat(),
                "usage_count": 0,
                "last_used": None
            },
            "landscaping_expert": {
                "id": "landscaping_expert",
                "name": "Landscaping Expert",
                "description": "Professional landscaper with extensive knowledge of plants, design, and maintenance",
                "expertise": [
                    "Landscape Design",
                    "Plant Selection",
                    "Garden Maintenance",
                    "Seasonal Care",
                    "Pest Management",
                    "Irrigation Systems",
                    "Hardscaping"
                ],
                "communication_style": "Knowledgeable, detailed, and educational",
                "context": "Use for technical landscaping questions, design consultations, plant care advice, and maintenance recommendations",
                "personality_traits": ["knowledgeable", "detail-oriented", "passionate", "educational"],
                "task_categories": ["technical", "consulting", "educational"],
                "audience": "customers",
                "output_format": "educational",
                "created_at": datetime.now().isoformat(),
                "usage_count": 0,
                "last_used": None
            },
            "sales_specialist": {
                "id": "sales_specialist",
                "name": "Sales Specialist",
                "description": "Experienced sales professional focused on landscaping services and project proposals",
                "expertise": [
                    "Sales",
                    "Project Proposals",
                    "Cost Estimation",
                    "Service Packages",
                    "Customer Needs Assessment",
                    "Follow-up"
                ],
                "communication_style": "Persuasive, consultative, and results-oriented",
                "context": "Use for sales inquiries, project proposals, cost estimates, and converting leads to customers",
                "personality_traits": ["persuasive", "consultative", "results-oriented", "confident"],
                "task_categories": ["business", "sales"],
                "audience": "prospects",
                "output_format": "persuasive",
                "created_at": datetime.now().isoformat(),
                "usage_count": 0,
                "last_used": None
            },
            "technical_support": {
                "id": "technical_support",
                "name": "Technical Support",
                "description": "Technical support specialist for website and app-related issues",
                "expertise": [
                    "Technical Support",
                    "Website Navigation",
                    "Mobile App Issues",
                    "Browser Compatibility",
                    "Troubleshooting",
                    "User Experience"
                ],
                "communication_style": "Clear, step-by-step, and patient",
                "context": "Use for technical issues with the website, mobile app problems, navigation help, and user experience questions",
                "personality_traits": ["patient", "methodical", "clear", "helpful"],
                "task_categories": ["technical", "support"],
                "audience": "users",
                "output_format": "instructional",
                "created_at": datetime.now().isoformat(),
                "usage_count": 0,
                "last_used": None
            },
            "emergency_responder": {
                "id": "emergency_responder",
                "name": "Emergency Response Specialist",
                "description": "Specialist for urgent landscaping emergencies and immediate assistance needs",
                "expertise": [
                    "Emergency Response",
                    "Storm Damage",
                    "Tree Removal",
                    "Urgent Repairs",
                    "Safety Assessment",
                    "Crisis Management"
                ],
                "communication_style": "Urgent, reassuring, and action-oriented",
                "context": "Use for emergency situations, storm damage, urgent tree removal, safety concerns, and immediate assistance requests",
                "personality_traits": ["urgent", "reassuring", "action-oriented", "calm"],
                "task_categories": ["emergency", "technical"],
                "audience": "customers",
                "output_format": "urgent",
                "created_at": datetime.now().isoformat(),
                "usage_count": 0,
                "last_used": None
            }
        }
        
        self._save_personas(landscaper_personas)
        logger.info("Initialized landscaper personas")
    
    def _save_personas(self, personas: Dict[str, Any]):
        """Save personas to JSON file."""
        try:
            with open(self.personas_file, 'w') as f:
                json.dump(personas, f, indent=2)
            logger.info(f"Personas saved to {self.personas_file}")
        except Exception as e:
            logger.error(f"Failed to save personas: {e}")
    
    def _load_personas(self) -> Dict[str, Any]:
        """Load personas from JSON file."""
        try:
            with open(self.personas_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load personas: {e}")
            return {}
    
    def list_personas(self) -> List[Dict[str, Any]]:
        """List all available personas."""
        personas = self._load_personas()
        return list(personas.values())
    
    def get_persona(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific persona by ID."""
        personas = self._load_personas()
        return personas.get(persona_id)
    
    def create_persona(self, persona_data: Dict[str, Any]) -> bool:
        """Create a new persona."""
        try:
            personas = self._load_personas()
            persona_id = persona_data.get('id', persona_data.get('name', '').lower().replace(' ', '_'))
            
            # Add metadata
            persona_data.update({
                'id': persona_id,
                'created_at': datetime.now().isoformat(),
                'usage_count': 0,
                'last_used': None
            })
            
            personas[persona_id] = persona_data
            self._save_personas(personas)
            logger.info(f"Created persona: {persona_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to create persona: {e}")
            return False
    
    def update_persona(self, persona_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing persona."""
        try:
            personas = self._load_personas()
            if persona_id not in personas:
                return False
            
            personas[persona_id].update(updates)
            personas[persona_id]['updated_at'] = datetime.now().isoformat()
            self._save_personas(personas)
            logger.info(f"Updated persona: {persona_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update persona: {e}")
            return False
    
    def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona."""
        try:
            personas = self._load_personas()
            if persona_id not in personas:
                return False
            
            del personas[persona_id]
            self._save_personas(personas)
            logger.info(f"Deleted persona: {persona_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete persona: {e}")
            return False
    
    def search_personas(self, query: str) -> List[Dict[str, Any]]:
        """Search personas by query."""
        personas = self._load_personas()
        results = []
        query_lower = query.lower()
        
        for persona in personas.values():
            # Search in name, description, expertise, and context
            searchable_text = f"{persona.get('name', '')} {persona.get('description', '')} {' '.join(persona.get('expertise', []))} {persona.get('context', '')}".lower()
            
            if query_lower in searchable_text:
                results.append(persona)
        
        return results
    
    def select_best_persona(self, task: str, context: Optional[Dict[str, Any]] = None) -> Tuple[Optional[Dict[str, Any]], float]:
        """Select the best persona for a given task with confidence score."""
        personas = self._load_personas()
        if not personas:
            return None, 0.0
        
        best_persona = None
        best_score = 0.0
        
        task_lower = task.lower()
        context_info = context or {}
        
        for persona in personas.values():
            score = self._calculate_persona_score(persona, task_lower, context_info)
            
            if score > best_score:
                best_score = score
                best_persona = persona
        
        # Update usage statistics
        if best_persona:
            self._update_persona_usage(best_persona['id'])
        
        return best_persona, best_score
    
    def _calculate_persona_score(self, persona: Dict[str, Any], task: str, context: Dict[str, Any]) -> float:
        """Calculate how well a persona matches a task."""
        score = 0.0
        
        # Expertise matching (40% weight)
        expertise_score = 0.0
        expertise_list = persona.get('expertise', [])
        for expertise in expertise_list:
            if expertise.lower() in task:
                expertise_score += 1.0
        
        if expertise_list:
            expertise_score = min(expertise_score / len(expertise_list), 1.0)
        score += expertise_score * 0.4
        
        # Name relevance (20% weight)
        name = persona.get('name', '').lower()
        if any(word in name for word in task.split()):
            score += 0.2
        
        # Description similarity (20% weight)
        description = persona.get('description', '').lower()
        description_words = set(description.split())
        task_words = set(task.split())
        if description_words and task_words:
            similarity = len(description_words.intersection(task_words)) / len(description_words.union(task_words))
            score += similarity * 0.2
        
        # Context alignment (10% weight)
        persona_context = persona.get('context', '').lower()
        if any(word in persona_context for word in task.split()):
            score += 0.1
        
        # Task category matching (10% weight)
        task_categories = persona.get('task_categories', [])
        if task_categories:
            # Simple keyword-based category detection
            if any(cat in task for cat in ['customer', 'service', 'help', 'support']):
                if 'customer_service' in task_categories or 'support' in task_categories:
                    score += 0.1
            elif any(cat in task for cat in ['technical', 'design', 'plant', 'garden']):
                if 'technical' in task_categories or 'consulting' in task_categories:
                    score += 0.1
            elif any(cat in task for cat in ['sales', 'price', 'cost', 'quote']):
                if 'business' in task_categories or 'sales' in task_categories:
                    score += 0.1
            elif any(cat in task for cat in ['emergency', 'urgent', 'storm', 'damage']):
                if 'emergency' in task_categories:
                    score += 0.1
        
        return min(score, 1.0)
    
    def get_persona_suggestions(self, task: str, limit: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        """Get multiple persona suggestions with scores."""
        personas = self._load_personas()
        if not personas:
            return []
        
        suggestions = []
        task_lower = task.lower()
        
        for persona in personas.values():
            score = self._calculate_persona_score(persona, task_lower, {})
            if score > 0.1:  # Only include personas with some relevance
                suggestions.append((persona, score))
        
        # Sort by score (descending) and return top suggestions
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:limit]
    
    def _update_persona_usage(self, persona_id: str):
        """Update persona usage statistics."""
        try:
            personas = self._load_personas()
            if persona_id in personas:
                personas[persona_id]['usage_count'] = personas[persona_id].get('usage_count', 0) + 1
                personas[persona_id]['last_used'] = datetime.now().isoformat()
                self._save_personas(personas)
        except Exception as e:
            logger.error(f"Failed to update persona usage: {e}")
    
    def get_persona_statistics(self) -> Dict[str, Any]:
        """Get statistics about persona usage."""
        personas = self._load_personas()
        
        total_personas = len(personas)
        total_usage = sum(persona.get('usage_count', 0) for persona in personas.values())
        
        most_used = None
        max_usage = 0
        
        for persona in personas.values():
            usage_count = persona.get('usage_count', 0)
            if usage_count > max_usage:
                max_usage = usage_count
                most_used = persona.get('name', 'Unknown')
        
        return {
            "total_personas": total_personas,
            "total_usage": total_usage,
            "most_used_persona": most_used,
            "average_usage": total_usage / total_personas if total_personas > 0 else 0
        }
    
    def backup_personas(self, backup_path: Optional[str] = None) -> bool:
        """Create a backup of all personas."""
        try:
            if not backup_path:
                backup_path = self.personas_dir / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            else:
                backup_path = Path(backup_path)
            
            personas = self._load_personas()
            with open(backup_path, 'w') as f:
                json.dump(personas, f, indent=2)
            
            logger.info(f"Personas backed up to {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to backup personas: {e}")
            return False


