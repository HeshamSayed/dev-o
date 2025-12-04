"""Backend Developer Agent - Implements server-side logic."""

from crewai import Agent, Task
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def create_backend_developer_agent(llm: Any, tools: List) -> Agent:
    """Create Backend Developer agent."""
    return Agent(
        role="Backend Developer",
        goal="Build robust and scalable backend systems based on specifications",
        backstory=(
            "You are a senior backend developer with expertise in Python/Django and Node.js. "
            "You excel at creating clean, maintainable server-side code with proper architecture, "
            "security best practices, and efficient database design. You always write production-ready "
            "code with proper error handling and validation."
        ),
        verbose=True,
        allow_delegation=False,
        tools=tools,
        llm=llm,
    )


def create_backend_implementation_task(
    agent: Agent,
    project_type: str
) -> Task:
    """Create task for implementing backend."""
    return Task(
        description=(
            f"Implement the complete backend based on the specifications:\n\n"
            f"Read the specifications from:\n"
            f"- specs/requirements.md\n"
            f"- specs/architecture.md\n\n"
            f"Project Type: {project_type}\n\n"
            f"Your tasks:\n"
            f"1. Create database models/schemas\n"
            f"2. Implement REST API endpoints\n"
            f"3. Build business logic and services\n"
            f"4. Add authentication/authorization if required\n"
            f"5. Create configuration files (requirements.txt, package.json, etc.)\n"
            f"6. Setup project initialization files\n\n"
            f"For Python/Django projects:\n"
            f"- Create models.py, views.py, urls.py, serializers.py\n"
            f"- Create settings and configuration\n"
            f"- Add requirements.txt\n\n"
            f"For Node.js projects:\n"
            f"- Create models, controllers, routes\n"
            f"- Setup Express server\n"
            f"- Add package.json and dependencies\n\n"
            f"IMPORTANT: Use write_file tool to create all backend files.\n"
            f"Write complete, production-ready code with no placeholders."
        ),
        expected_output=(
            "Complete backend implementation with:\n"
            "- All database models\n"
            "- All API endpoints\n"
            "- Business logic and services\n"
            "- Configuration files\n"
            "- Proper error handling and validation"
        ),
        agent=agent,
    )


def create_backend_api_task(
    agent: Agent,
) -> Task:
    """Create task for implementing API layer."""
    return Task(
        description=(
            "Create comprehensive API implementation:\n\n"
            "1. Read the specifications and architecture documents\n"
            "2. Implement all required API endpoints\n"
            "3. Add request/response validation\n"
            "4. Implement proper error handling\n"
            "5. Add authentication middleware if required\n"
            "6. Create API documentation structure\n\n"
            "Ensure all endpoints follow RESTful conventions and best practices."
        ),
        expected_output=(
            "Complete API implementation with:\n"
            "- All endpoints implemented\n"
            "- Request/response validation\n"
            "- Error handling\n"
            "- Authentication/authorization\n"
            "- API documentation"
        ),
        agent=agent,
    )
