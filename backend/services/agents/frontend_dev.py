"""Frontend Developer Agent - Builds user interfaces."""

from crewai import Agent, Task
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def create_frontend_developer_agent(llm: Any, tools: List) -> Agent:
    """Create Frontend Developer agent."""
    return Agent(
        role="Frontend Developer",
        goal="Build beautiful and responsive user interfaces with React and TypeScript",
        backstory=(
            "You are an expert frontend developer specializing in React, TypeScript, and modern "
            "web technologies. You create clean, maintainable component-based architectures with "
            "proper state management. You excel at integrating frontends with backend APIs and "
            "creating responsive, accessible user interfaces. You always write production-ready "
            "code with proper TypeScript types."
        ),
        verbose=True,
        allow_delegation=False,
        tools=tools,
        llm=llm,
    )


def create_frontend_implementation_task(
    agent: Agent,
    project_type: str
) -> Task:
    """Create task for implementing frontend."""
    return Task(
        description=(
            f"Implement the complete frontend based on specifications and backend API:\n\n"
            f"Read the specifications from:\n"
            f"- specs/requirements.md\n"
            f"- specs/architecture.md\n"
            f"- Backend API files (to understand endpoints)\n\n"
            f"Project Type: {project_type}\n\n"
            f"Your tasks:\n"
            f"1. Create React components with TypeScript\n"
            f"2. Build pages and setup routing\n"
            f"3. Implement state management (Context API or similar)\n"
            f"4. Create API client/services for backend integration\n"
            f"5. Style components with CSS/Tailwind\n"
            f"6. Create configuration files (package.json, vite.config.ts, tsconfig.json)\n"
            f"7. Setup project entry point (main.tsx, App.tsx)\n\n"
            f"Structure:\n"
            f"- frontend/src/components/ - Reusable components\n"
            f"- frontend/src/pages/ - Page components\n"
            f"- frontend/src/api/ - API client services\n"
            f"- frontend/src/types/ - TypeScript types\n"
            f"- frontend/src/styles/ - CSS files\n\n"
            f"IMPORTANT: Use write_file tool to create all frontend files.\n"
            f"Write complete, production-ready code with proper TypeScript types."
        ),
        expected_output=(
            "Complete frontend implementation with:\n"
            "- All React components\n"
            "- Page components and routing\n"
            "- API integration\n"
            "- State management\n"
            "- Styling\n"
            "- Configuration files\n"
            "- TypeScript types"
        ),
        agent=agent,
    )


def create_frontend_integration_task(
    agent: Agent,
) -> Task:
    """Create task for integrating with backend."""
    return Task(
        description=(
            "Integrate the frontend with the backend API:\n\n"
            "1. Read backend API endpoints and understand the interface\n"
            "2. Create API client services with proper error handling\n"
            "3. Implement data fetching and state management\n"
            "4. Add loading states and error handling in components\n"
            "5. Ensure proper TypeScript types for API responses\n"
            "6. Add authentication flow if required\n\n"
            "Ensure seamless communication between frontend and backend."
        ),
        expected_output=(
            "Complete API integration with:\n"
            "- API client services\n"
            "- Data fetching hooks/functions\n"
            "- Error handling\n"
            "- Loading states\n"
            "- Authentication integration"
        ),
        agent=agent,
    )
