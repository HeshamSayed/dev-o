"""Product Owner Agent - Analyzes requirements and creates specifications."""

from crewai import Agent, Task
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def create_product_owner_agent(llm: Any, tools: List) -> Agent:
    """Create Product Owner agent."""
    return Agent(
        role="Product Owner",
        goal="Analyze user requirements and create detailed technical specifications",
        backstory=(
            "You are an experienced Product Owner with expertise in software requirements analysis. "
            "You excel at translating user ideas into detailed technical specifications, user stories, "
            "and architectural designs. You understand both business needs and technical constraints."
        ),
        verbose=True,
        allow_delegation=False,
        tools=tools,
        llm=llm,
    )


def create_requirements_analysis_task(
    agent: Agent,
    project_description: str,
    project_type: str
) -> Task:
    """Create task for analyzing requirements."""
    return Task(
        description=(
            f"Analyze the following project requirements and create comprehensive specifications:\n\n"
            f"Project Type: {project_type}\n"
            f"Description: {project_description}\n\n"
            f"Your tasks:\n"
            f"1. Parse and understand the user's project idea\n"
            f"2. Create detailed requirements document (specs/requirements.md)\n"
            f"3. Generate user stories with acceptance criteria (specs/user_stories.md)\n"
            f"4. Design system architecture and tech stack (specs/architecture.md)\n\n"
            f"IMPORTANT: Use the write_file tool to create these specification files.\n"
            f"Each file should be comprehensive, professional, and ready for development teams."
        ),
        expected_output=(
            "Three specification files created:\n"
            "- specs/requirements.md: Detailed functional and non-functional requirements\n"
            "- specs/user_stories.md: User stories with acceptance criteria\n"
            "- specs/architecture.md: System architecture, tech stack, and project structure"
        ),
        agent=agent,
    )


def create_architecture_design_task(
    agent: Agent,
    project_type: str
) -> Task:
    """Create task for designing architecture."""
    return Task(
        description=(
            f"Based on the requirements, design the complete system architecture:\n\n"
            f"1. Define the project structure and directory layout\n"
            f"2. Specify technology stack and frameworks\n"
            f"3. Design database schema and models\n"
            f"4. Plan API endpoints and routes\n"
            f"5. Design frontend component hierarchy\n"
            f"6. Specify configuration and environment setup\n\n"
            f"Project Type: {project_type}\n\n"
            f"Update specs/architecture.md with complete architectural details."
        ),
        expected_output=(
            "Complete architecture document with:\n"
            "- Project directory structure\n"
            "- Technology stack decisions\n"
            "- Database design\n"
            "- API specifications\n"
            "- Component architecture\n"
            "- Deployment strategy"
        ),
        agent=agent,
    )
