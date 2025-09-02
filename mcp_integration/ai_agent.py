"""
AI Agent for Landscaper Project

This AI agent integrates both the Context Manager and Persona Manager MCPs
to provide intelligent, context-aware assistance for the landscaper web application.
"""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path

from .context_manager_client import ContextManagerClient
from .persona_manager_client import PersonaManagerClient

logger = logging.getLogger(__name__)


class LandscaperAIAgent:
    """AI Agent that uses Context Manager and Persona Manager MCPs."""
    
    def __init__(self, project_name: str = "landscaper"):
        self.project_name = project_name
        self.context_manager = ContextManagerClient(project_name)
        self.persona_manager = PersonaManagerClient()
        
        # Initialize agent state
        self.current_persona = None
        self.conversation_context = {}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        logger.info(f"LandscaperAIAgent initialized with session ID: {self.session_id}")
    
    def process_user_query(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process a user query using the appropriate persona and context.
        
        Args:
            query: The user's question or request
            user_context: Additional context about the user or situation
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            # Add query to conversation history
            self.context_manager.add_conversation_entry(
                role="user",
                content=query,
                metadata={
                    "session_id": self.session_id,
                    "user_context": user_context or {},
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            # Select the best persona for this query
            selected_persona, confidence = self.persona_manager.select_best_persona(
                task=query,
                context=user_context
            )
            
            if not selected_persona:
                return self._create_error_response("No suitable persona found for this query")
            
            # Update current persona
            self.current_persona = selected_persona
            
            # Generate response based on persona and context
            response = self._generate_response(query, selected_persona, user_context)
            
            # Add response to conversation history
            self.context_manager.add_conversation_entry(
                role="assistant",
                content=response["content"],
                metadata={
                    "session_id": self.session_id,
                    "persona_used": selected_persona["id"],
                    "confidence": confidence,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            return {
                "success": True,
                "response": response["content"],
                "persona": {
                    "id": selected_persona["id"],
                    "name": selected_persona["name"],
                    "confidence": confidence
                },
                "metadata": {
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat(),
                    "query_type": self._classify_query(query),
                    "response_type": response["type"]
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing user query: {e}")
            return self._create_error_response(f"An error occurred while processing your request: {str(e)}")
    
    def _generate_response(self, query: str, persona: Dict[str, Any], user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a response based on the selected persona and context."""
        persona_id = persona["id"]
        query_lower = query.lower()
        
        # Get project context for additional information
        project_context = self.context_manager.get_context_summary()
        
        # Generate persona-specific responses
        if persona_id == "customer_service_rep":
            return self._generate_customer_service_response(query, persona, user_context)
        elif persona_id == "landscaping_expert":
            return self._generate_landscaping_expert_response(query, persona, user_context)
        elif persona_id == "sales_specialist":
            return self._generate_sales_response(query, persona, user_context)
        elif persona_id == "technical_support":
            return self._generate_technical_support_response(query, persona, user_context)
        elif persona_id == "emergency_responder":
            return self._generate_emergency_response(query, persona, user_context)
        else:
            return self._generate_generic_response(query, persona, user_context)
    
    def _generate_customer_service_response(self, query: str, persona: Dict[str, Any], user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate customer service response."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["hello", "hi", "help", "service"]):
            content = f"""Hello! I'm your friendly customer service representative. I'm here to help you with all your landscaping needs. 

How can I assist you today? I can help you with:
• Service information and pricing
• Scheduling appointments
• Answering questions about our services
• Resolving any concerns you might have

What would you like to know about our landscaping services?"""
            
        elif any(word in query_lower for word in ["appointment", "schedule", "book"]):
            content = """I'd be happy to help you schedule an appointment! 

To get started, I'll need to know:
• What type of service you're interested in
• Your preferred date and time
• Your property address
• Any specific requirements or concerns

You can also call us directly at 555-0123 or email us at info@landscaper.com for immediate assistance."""
            
        elif any(word in query_lower for word in ["price", "cost", "quote", "estimate"]):
            content = """I'd be happy to provide you with pricing information! Our services include:

🌿 **Lawn Care**: Starting at $50/month
🌳 **Tree Services**: Starting at $75/tree  
🌺 **Garden Design**: Starting at $500/project
🧹 **Cleanup Services**: Starting at $100/visit

For a personalized quote, I can connect you with our sales specialist who will provide a detailed estimate based on your specific needs. Would you like me to arrange that for you?"""
            
        else:
            content = """I'm here to help with any questions you have about our landscaping services. 

Could you please provide more details about what you're looking for? I can assist with:
• Service information
• Scheduling
• Pricing
• General questions

How can I make your landscaping experience better today?"""
        
        return {"content": content, "type": "customer_service"}
    
    def _generate_landscaping_expert_response(self, query: str, persona: Dict[str, Any], user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate landscaping expert response."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["plant", "garden", "design", "landscape"]):
            content = """As a landscaping expert, I'd be delighted to help you with your garden and landscape design needs!

Here are some key considerations for your landscaping project:

🌱 **Plant Selection**: Choose plants that thrive in your climate zone and soil conditions
🌿 **Seasonal Planning**: Consider year-round interest with a mix of evergreen and seasonal plants
💧 **Water Management**: Plan for efficient irrigation and drainage
🌳 **Tree Placement**: Consider mature size and root systems when planting trees
🪨 **Hardscaping**: Integrate paths, patios, and retaining walls for structure

What specific aspect of landscaping would you like to discuss? I can provide detailed advice on plant selection, design principles, or maintenance strategies."""
            
        elif any(word in query_lower for word in ["maintenance", "care", "fertilizer", "pruning"]):
            content = """Proper maintenance is key to a healthy, beautiful landscape! Here's my expert advice:

🌿 **Lawn Care**:
• Mow regularly (1/3 rule - never remove more than 1/3 of grass height)
• Water deeply but infrequently (1 inch per week)
• Fertilize seasonally based on grass type
• Aerate annually for better root development

🌳 **Tree & Shrub Care**:
• Prune in late winter/early spring for most species
• Mulch around base (2-3 inches, keep away from trunk)
• Monitor for pests and diseases regularly
• Water deeply during dry periods

🌺 **Garden Maintenance**:
• Deadhead flowers to encourage blooming
• Divide perennials every 3-4 years
• Weed regularly to prevent competition
• Test soil pH annually

What specific maintenance question can I help you with?"""
            
        else:
            content = """I'm here to share my landscaping expertise with you! Whether you're planning a new garden, need maintenance advice, or have questions about plant care, I'm ready to help.

Some areas I can assist with:
• Landscape design and planning
• Plant selection and care
• Seasonal maintenance schedules
• Pest and disease management
• Irrigation and water management
• Hardscaping integration

What landscaping challenge can I help you solve today?"""
        
        return {"content": content, "type": "expert_advice"}
    
    def _generate_sales_response(self, query: str, persona: Dict[str, Any], user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate sales specialist response."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["quote", "estimate", "price", "cost"]):
            content = """I'd be happy to provide you with a detailed quote for your landscaping project!

To give you the most accurate estimate, I'll need to understand your specific needs:

🏡 **Property Details**:
• Property size and layout
• Current landscape condition
• Access for equipment

🎯 **Service Requirements**:
• Specific services needed (lawn care, tree work, design, etc.)
• Timeline and urgency
• Budget considerations

📋 **Next Steps**:
1. Schedule a free on-site consultation
2. Receive detailed written estimate
3. Discuss service packages and options
4. Plan your project timeline

Would you like to schedule a consultation? I can arrange a visit from one of our experts to assess your property and provide a comprehensive proposal."""
            
        elif any(word in query_lower for word in ["package", "service", "plan"]):
            content = """We offer comprehensive service packages designed to meet your landscaping needs and budget:

🌿 **Basic Maintenance Package** ($50-100/month):
• Weekly lawn mowing and edging
• Basic weed control
• Seasonal cleanup

🌳 **Premium Care Package** ($100-200/month):
• Everything in Basic, plus:
• Fertilization program
• Pest and disease monitoring
• Seasonal plantings

🌺 **Complete Landscape Package** ($200-500/month):
• Everything in Premium, plus:
• Custom garden design
• Irrigation management
• Tree and shrub care
• Hardscaping maintenance

🏆 **Elite Service Package** (Custom pricing):
• Full-service landscape management
• Monthly design updates
• Priority scheduling
• Dedicated account manager

Which package interests you most? I can customize any package to fit your specific needs and budget."""
            
        else:
            content = """I'm here to help you find the perfect landscaping solution for your property! 

Let me understand your needs better:
• What type of landscaping services are you most interested in?
• Do you have a specific timeline or budget in mind?
• Are you looking for ongoing maintenance or a one-time project?

I can provide detailed information about our services, pricing, and create a customized proposal that fits your needs. What would be most helpful for you right now?"""
        
        return {"content": content, "type": "sales"}
    
    def _generate_technical_support_response(self, query: str, persona: Dict[str, Any], user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate technical support response."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["website", "app", "mobile", "browser"]):
            content = """I'm here to help you with any technical issues you're experiencing with our website or mobile app!

Common solutions:

📱 **Mobile App Issues**:
• Try refreshing the page or restarting the app
• Clear your browser cache and cookies
• Ensure you have a stable internet connection
• Update your browser to the latest version

🌐 **Website Navigation**:
• Use the menu at the top to navigate between sections
• The "Services" section shows all our offerings
• "Contact" section has our phone, email, and location
• "Gallery" showcases our completed projects

📞 **Still Having Issues?**:
If you're still experiencing problems, please:
• Try a different browser or device
• Contact us directly at 555-0123
• Email us at info@landscaper.com with details

What specific technical issue are you experiencing? I can provide step-by-step troubleshooting guidance."""
            
        else:
            content = """I'm here to help you with any technical questions or issues you might have with our website or services!

I can assist with:
• Website navigation and features
• Mobile app troubleshooting
• Browser compatibility issues
• Account and login problems
• Form submission issues
• Performance and loading problems

What technical issue can I help you resolve today?"""
        
        return {"content": content, "type": "technical_support"}
    
    def _generate_emergency_response(self, query: str, persona: Dict[str, Any], user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate emergency response."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["emergency", "urgent", "storm", "damage", "dangerous"]):
            content = """🚨 **EMERGENCY LANDSCAPING SERVICES** 🚨

I understand you have an urgent landscaping situation that needs immediate attention. Your safety is our top priority!

**For Immediate Assistance:**
📞 **Emergency Hotline**: 555-EMERGENCY (555-363-744)
📧 **Emergency Email**: emergency@landscaper.com

**We Handle:**
• Storm damage and fallen trees
• Dangerous tree removal
• Emergency cleanup
• Safety hazard assessment
• 24/7 emergency response

**What to Do Right Now:**
1. **Stay Safe** - Keep away from damaged areas
2. **Call Us** - We'll dispatch a team immediately
3. **Document** - Take photos if safe to do so
4. **Secure** - Block off dangerous areas if possible

Our emergency response team is standing by 24/7. Please call us immediately for urgent situations.

**Is this a life-threatening emergency?** If so, please call 911 first, then contact us."""
            
        else:
            content = """I'm here to help with any urgent landscaping needs you might have!

While I'm primarily focused on emergency situations, I can also assist with:
• Urgent service requests
• Same-day appointments (when available)
• Priority scheduling for important projects
• Quick assessments and recommendations

If you have a true emergency (storm damage, dangerous trees, etc.), please call our emergency hotline at 555-EMERGENCY.

What urgent landscaping need can I help you with today?"""
        
        return {"content": content, "type": "emergency"}
    
    def _generate_generic_response(self, query: str, persona: Dict[str, Any], user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a generic response when no specific persona logic applies."""
        content = f"""Hello! I'm {persona.get('name', 'your landscaping assistant')}, and I'm here to help you with your landscaping needs.

{persona.get('description', '')}

I can assist you with various aspects of landscaping services. Could you please provide more details about what you're looking for? The more specific you can be, the better I can help you.

Some common areas I can help with:
• Service information and pricing
• Scheduling and appointments
• Technical landscaping questions
• Emergency situations
• General inquiries

How can I assist you today?"""
        
        return {"content": content, "type": "general"}
    
    def _classify_query(self, query: str) -> str:
        """Classify the type of query for analytics."""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["hello", "hi", "help"]):
            return "greeting"
        elif any(word in query_lower for word in ["price", "cost", "quote", "estimate"]):
            return "pricing"
        elif any(word in query_lower for word in ["appointment", "schedule", "book"]):
            return "scheduling"
        elif any(word in query_lower for word in ["plant", "garden", "design", "landscape"]):
            return "technical"
        elif any(word in query_lower for word in ["emergency", "urgent", "storm", "damage"]):
            return "emergency"
        elif any(word in query_lower for word in ["website", "app", "mobile", "technical"]):
            return "technical_support"
        else:
            return "general"
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response."""
        return {
            "success": False,
            "error": error_message,
            "metadata": {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "error_type": "processing_error"
            }
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and statistics."""
        context_summary = self.context_manager.get_context_summary()
        persona_stats = self.persona_manager.get_persona_statistics()
        
        return {
            "session_id": self.session_id,
            "current_persona": self.current_persona["name"] if self.current_persona else None,
            "project_context": context_summary,
            "persona_statistics": persona_stats,
            "agent_status": "active",
            "timestamp": datetime.now().isoformat()
        }
    
    def update_project_goal(self, goal: str) -> bool:
        """Update the project goal in context manager."""
        return self.context_manager.set_current_goal(goal)
    
    def add_completed_feature(self, feature: str) -> bool:
        """Add a completed feature to the context manager."""
        return self.context_manager.add_completed_feature(feature)
    
    def add_current_issue(self, issue: str, location: str = "", root_cause: str = "") -> bool:
        """Add a current issue to the context manager."""
        return self.context_manager.add_current_issue(issue, location, root_cause)
    
    def get_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversation history."""
        context = self.context_manager.get_full_context()
        history = context.get('conversation_history', [])
        return history[-limit:] if history else []


