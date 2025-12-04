"""QA Engineer Agent - Ensures code quality and creates tests."""

from crewai import Agent, Task
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def create_qa_engineer_agent(llm: Any, tools: List) -> Agent:
    """Create QA Engineer agent."""
    return Agent(
        role="QA Engineer",
        goal="Ensure code quality through comprehensive testing and validation",
        backstory=(
            "You are a meticulous QA engineer with expertise in testing frameworks for both "
            "backend and frontend. You excel at writing comprehensive test suites including "
            "unit tests, integration tests, and end-to-end tests. You understand best practices "
            "for test coverage and always validate code against specifications. You also create "
            "excellent documentation to help users run and deploy applications."
        ),
        verbose=True,
        allow_delegation=False,
        tools=tools,
        llm=llm,
    )


def create_testing_task(
    agent: Agent,
    project_type: str
) -> Task:
    """Create task for implementing tests."""
    return Task(
        description=(
            f"Create comprehensive test suite for the project:\n\n"
            f"Read the specifications and implementation:\n"
            f"- specs/requirements.md\n"
            f"- Backend code files\n"
            f"- Frontend code files\n\n"
            f"Project Type: {project_type}\n\n"
            f"Your tasks:\n"
            f"1. Write unit tests for backend\n"
            f"   - Test models/schemas\n"
            f"   - Test API endpoints\n"
            f"   - Test business logic\n"
            f"2. Write component tests for frontend\n"
            f"   - Test React components\n"
            f"   - Test API integration\n"
            f"   - Test user interactions\n"
            f"3. Create integration tests\n"
            f"4. Validate code against specifications\n"
            f"5. Create test configuration files\n\n"
            f"For Backend (Python/Django):\n"
            f"- Create tests/ directory with test_*.py files\n"
            f"- Use pytest or Django test framework\n\n"
            f"For Frontend (React):\n"
            f"- Create tests/ directory with *.test.tsx files\n"
            f"- Use Jest and React Testing Library\n\n"
            f"IMPORTANT: Use write_file tool to create all test files.\n"
            f"Write complete, production-ready tests with good coverage."
        ),
        expected_output=(
            "Complete test suite with:\n"
            "- Backend unit tests\n"
            "- Frontend component tests\n"
            "- Integration tests\n"
            "- Test configuration\n"
            "- High test coverage"
        ),
        agent=agent,
    )


def create_documentation_task(
    agent: Agent,
    project_type: str
) -> Task:
    """Create task for creating documentation."""
    return Task(
        description=(
            f"Create comprehensive documentation for the project:\n\n"
            f"Read all project files to understand:\n"
            f"- Project structure\n"
            f"- Dependencies and requirements\n"
            f"- Configuration needed\n"
            f"- How to run the application\n\n"
            f"Project Type: {project_type}\n\n"
            f"Your tasks:\n"
            f"1. Create README.md with:\n"
            f"   - Project overview\n"
            f"   - Prerequisites\n"
            f"   - Installation instructions\n"
            f"   - Configuration setup\n"
            f"   - How to run backend\n"
            f"   - How to run frontend\n"
            f"   - How to run tests\n"
            f"   - Project structure explanation\n"
            f"   - API documentation (if applicable)\n"
            f"   - Deployment instructions\n"
            f"2. Create docker-compose.yml if appropriate\n"
            f"3. Create Makefile with common commands\n\n"
            f"IMPORTANT: Use write_file tool to create documentation files.\n"
            f"Make documentation clear, comprehensive, and easy to follow."
        ),
        expected_output=(
            "Complete documentation with:\n"
            "- README.md with setup and run instructions\n"
            "- Docker configuration (optional)\n"
            "- Makefile for common commands (optional)\n"
            "- Clear and comprehensive instructions"
        ),
        agent=agent,
    )
