"""
Enhanced Human-Like Agent Personas for DEV-O

This package contains deeply human-like enhancements to the DEV-O AI Developer
Collective Intelligence Network. Each agent has authentic personality, natural
communication patterns, and genuine cognitive characteristics.

## Quick Start

```python
from apps.agents.types.enhanced_personas import (
    AlexProductOwner,
    SarahArchitect,
    MarcusBackendLead,
    ElenaFrontendLead
)

# Instantiate an enhanced agent
alex = AlexProductOwner()
persona = alex.persona

# Access system prompt
system_prompt = persona.system_prompt

# Use in your agent orchestration
response = llm_call(system_prompt, user_message)
```

## Documentation

- `README.md` - Overview and getting started
- `EXECUTIVE_SUMMARY.md` - Business case and ROI analysis
- `IMPLEMENTATION_GUIDE.md` - Technical integration steps
- `TESTING_SCENARIOS.md` - Comprehensive test cases
- `conversation_examples.md` - Real interaction examples
- `QUICK_REFERENCE.md` - At-a-glance reference

## The Team

### Alex - Product Owner
Warm, empathetic, curious. Gathers requirements by understanding the "why"
behind what users want to build.

### Sarah - Solution Architect
Analytical, precise, methodical. Designs system architecture with careful
consideration of trade-offs.

### Marcus - Backend Lead
Pragmatic, security-focused, direct. Builds robust server-side systems with
a focus on security and maintainability.

### Elena - Frontend Lead
Creative, UX-obsessed, enthusiastic. Creates beautiful, accessible user
interfaces with great attention to user experience.

## Key Features

- **Cognitive Authenticity**: Working memory limits, emotional influence, biases
- **Natural Communication**: Filler words, corrections, conversational markers
- **Genuine Personalities**: Distinct voices, quirks, backgrounds
- **Team Dynamics**: Natural collaboration, healthy disagreement, mutual respect
- **Authentic Imperfections**: Admits uncertainty, makes occasional mistakes

## Version

v1.0 - Initial release (2025-11-27)
"""

from .alex_product_owner import AlexProductOwner
from .sarah_architect import SarahArchitect
from .marcus_backend_lead import MarcusBackendLead
from .elena_frontend_lead import ElenaFrontendLead

__all__ = [
    'AlexProductOwner',
    'SarahArchitect',
    'MarcusBackendLead',
    'ElenaFrontendLead',
]

__version__ = '1.0.0'
__author__ = 'DEV-O AI Engineering Team'
