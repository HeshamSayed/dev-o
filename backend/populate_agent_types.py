"""
Populate AgentType models from agent type definitions.
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devo.settings')
django.setup()

from apps.agents.models import AgentType
from apps.agents.types.enhanced_personas.alex_product_owner import AlexProductOwner
from apps.agents.types.enhanced_personas.sarah_architect import SarahArchitect
from apps.agents.types.enhanced_personas.marcus_backend_lead import MarcusBackendLead
from apps.agents.types.enhanced_personas.elena_frontend_lead import ElenaFrontendLead

def populate_agent_types():
    """Create or update agent types in database."""

    # Clean up any old product_owner role (replaced by orchestrator with Alex's persona)
    AgentType.objects.filter(role='product_owner').delete()
    print("Cleaned up old product_owner role entries")

    agent_classes = [
        AlexProductOwner(),
        SarahArchitect(),
        MarcusBackendLead(),
        ElenaFrontendLead(),
    ]

    # Enhanced persona temperature settings
    temperature_settings = {
        'product_owner': 0.8,  # Alex - Higher for conversational warmth
        'architect': 0.7,      # Sarah - Balanced for technical precision with personality
        'backend_lead': 0.6,   # Marcus - Lower for code generation accuracy
        'frontend_lead': 0.75, # Elena - Balanced for creativity and code
    }

    for agent_class in agent_classes:
        persona = agent_class.persona

        agent_type, created = AgentType.objects.update_or_create(
            role=persona.role,
            defaults={
                'name': persona.name,
                'description': f"{persona.name} agent with enhanced human-like persona",
                'system_prompt': persona.system_prompt,
                'available_tools': persona.available_tools,
                'can_hire': persona.can_hire or [],
                'hierarchy_level': persona.hierarchy_level,
                'default_model': 'deepseek-r1:7b',  # Can be updated to claude-sonnet-4-5 or gpt-4
                'default_temperature': temperature_settings.get(persona.role, 0.7),
                'max_iterations': persona.max_iterations,
                'is_active': True
            }
        )

        action = "Created" if created else "Updated"
        print(f"{action} AgentType: {agent_type.name} (role={agent_type.role}, level={agent_type.hierarchy_level})")

if __name__ == '__main__':
    print("Populating agent types...")
    populate_agent_types()
    print("\nDone!")

    # List all agent types
    print("\nAll agent types in database:")
    for agent_type in AgentType.objects.all():
        print(f"  - {agent_type.name} (role={agent_type.role}, can_hire={agent_type.can_hire})")
