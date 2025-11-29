"""
Orchestrator Agent

The Orchestrator is the first agent that interacts with the user.
It coordinates the overall project and hires the Architect.

Now using Alex's enhanced human-like persona for authentic, natural interactions.
"""

from typing import Dict, Any
from .base import BaseAgentType, AgentPersona
from .enhanced_personas.alex_product_owner import AlexProductOwner


class OrchestratorAgent(AlexProductOwner):
    """
    Orchestrator Agent - Project Coordinator

    Now powered by Alex's enhanced human-like persona.

    Alex is a warm, empathetic Product Owner with 8 years of experience
    who genuinely cares about understanding user needs and building great products.

    The enhanced persona brings:
    - Natural, conversational communication
    - Genuine curiosity and active listening
    - Human-like cognitive patterns (working memory, reconstructive memory, emotional influence)
    - Authentic team coordination with Sarah, Marcus, and Elena
    - Context-aware collaboration across the development team
    """

    @property
    def persona(self) -> AgentPersona:
        """Override to use 'orchestrator' role while keeping Alex's persona."""
        base_persona = super().persona
        return AgentPersona(
            name=base_persona.name,
            role="orchestrator",  # Keep orchestrator role for system compatibility
            hierarchy_level=base_persona.hierarchy_level,
            system_prompt=base_persona.system_prompt,
            available_tools=base_persona.available_tools,
            can_hire=base_persona.can_hire,
            thinking_style=base_persona.thinking_style,
            verbosity=base_persona.verbosity,
            max_iterations=base_persona.max_iterations,
        )
