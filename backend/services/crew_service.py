"""CrewAI orchestration service for multi-agent development team."""

import logging
from typing import Dict, Any, List, AsyncGenerator
from datetime import datetime
from django.conf import settings
from crewai import Crew, Process, LLM
from channels.db import database_sync_to_async
import asyncio

from apps.projects.models import Project, ProjectFile
from .agents.tools.file_tools import create_file_tools
from .agents.product_owner import (
    create_product_owner_agent,
    create_requirements_analysis_task,
    create_architecture_design_task,
)
from .agents.backend_dev import (
    create_backend_developer_agent,
    create_backend_implementation_task,
    create_backend_api_task,
)
from .agents.frontend_dev import (
    create_frontend_developer_agent,
    create_frontend_implementation_task,
    create_frontend_integration_task,
)
from .agents.qa_engineer import (
    create_qa_engineer_agent,
    create_testing_task,
    create_documentation_task,
)

logger = logging.getLogger(__name__)


class CrewService:
    """Service for orchestrating CrewAI multi-agent team."""

    def __init__(self):
        """Initialize CrewAI service."""
        self.file_storage: Dict[str, str] = {}
        self.verbose = getattr(settings, 'CREWAI_VERBOSE', True)
        self.max_iterations = getattr(settings, 'CREWAI_MAX_ITERATIONS', 10)
        self.memory_enabled = getattr(settings, 'CREWAI_MEMORY', True)
        # Session storage for maintaining context across requests
        self.session_contexts: Dict[str, Dict[str, Any]] = {}
        
    def _create_llm(self) -> LLM:
        """Create LLM instance for CrewAI agents."""
        # Use CrewAI's native LLM integration with external Mistral 7B service
        ai_service_config = settings.AI_SERVICE
        
        # CrewAI supports OpenAI-compatible APIs
        # Configure with token limits for Mistral 7B model
        return LLM(
            model=ai_service_config.get('DEFAULT_MODEL', 'mistral-7b'),
            base_url=ai_service_config.get('BASE_URL', 'http://34.136.165.200:7000'),
            api_key=ai_service_config.get('API_KEY', 'dummy-key'),
            temperature=0.7,
            max_tokens=ai_service_config.get('MAX_OUTPUT_TOKENS', 2048),
            timeout=ai_service_config.get('TIMEOUT', 120),
        )

    def get_or_create_session(self, project_id: str) -> Dict[str, Any]:
        """Get or create session context for a project."""
        if project_id not in self.session_contexts:
            self.session_contexts[project_id] = {
                'project_id': project_id,
                'execution_count': 0,
                'last_execution': None,
                'conversation_history': [],
                'completed_agents': [],  # Track which agents completed successfully
                'last_error': None,  # Store last error for continuation
                'can_continue': False,  # Flag to indicate if continuation is possible
            }
        return self.session_contexts[project_id]

    def update_session_context(self, project_id: str, key: str, value: Any):
        """Update session context for a project."""
        session = self.get_or_create_session(project_id)
        session[key] = value
        logger.info(f"[CREW] Updated session context for project {project_id}: {key}")

    async def execute_development_crew(
        self,
        project: Project,
        project_description: str,
        continue_from_last: bool = False,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute the full development crew in sequential order with session memory.
        
        Pipeline: Product Owner → Backend Dev → Frontend Dev → QA Engineer
        
        Session memory maintains context across multiple executions for the same project.
        
        Args:
            project: The project to work on
            project_description: User's request/description
            continue_from_last: If True, continue from the last failed agent instead of starting over
        """
        try:
            project_id_str = str(project.id)
            logger.info(f"[CREW] Starting development crew for project {project_id_str}")
            
            # Get or create session context
            session = self.get_or_create_session(project_id_str)
            session['execution_count'] += 1
            session['last_execution'] = project_description
            session['can_continue'] = False  # Reset continuation flag
            session['last_error'] = None  # Clear previous errors
            
            # Determine starting point
            if continue_from_last and session.get('completed_agents'):
                logger.info(f"[CREW] Continuing from last failed agent. Completed: {session['completed_agents']}")
                yield {
                    'type': 'crew_continuation',
                    'message': f"Continuing from where we left off. Completed agents: {', '.join(session['completed_agents'])}",
                    'completed_agents': session['completed_agents']
                }
            else:
                # Starting fresh - clear completed agents
                session['completed_agents'] = []
            
            # Add to conversation history
            session['conversation_history'].append({
                'role': 'user',
                'content': project_description,
                'timestamp': datetime.now().isoformat(),
                'continuation': continue_from_last
            })
            
            logger.info(f"[CREW] Session execution count: {session['execution_count']}")
            
            # Reset file storage for this execution but keep session context
            self.file_storage = {}
            
            # Create shared tools
            tools = create_file_tools(self.file_storage)
            
            # Create LLM
            llm = self._create_llm()
            
            # Create agents
            product_owner = create_product_owner_agent(llm, tools)
            backend_dev = create_backend_developer_agent(llm, tools)
            frontend_dev = create_frontend_developer_agent(llm, tools)
            qa_engineer = create_qa_engineer_agent(llm, tools)
            
            logger.info("[CREW] Agents created successfully")
            
            # Define agent pipeline
            agents_pipeline = [
                ('Product Owner', product_owner, self._execute_product_owner, [project, project_description]),
                ('Backend Developer', backend_dev, self._execute_backend_developer, [project]),
                ('Frontend Developer', frontend_dev, self._execute_frontend_developer, [project]),
                ('QA Engineer', qa_engineer, self._execute_qa_engineer, [project]),
            ]
            
            # Yield agent initialization
            yield {
                'type': 'crew_init',
                'agents': [
                    {'name': name, 'status': 'completed' if name in session['completed_agents'] else 'initialized'}
                    for name, _, _, _ in agents_pipeline
                ]
            }
            
            # Execute agents in sequence
            for agent_name, agent, execute_func, args in agents_pipeline:
                # Skip if already completed (continuation scenario)
                if agent_name in session['completed_agents']:
                    logger.info(f"[CREW] Skipping {agent_name} - already completed")
                    continue
                
                try:
                    # Signal agent starting
                    yield {'type': 'agent_started', 'agent': agent_name}
                    logger.info(f"[CREW] Starting {agent_name} phase...")
                    
                    files_before = len(self.file_storage)
                    
                    # Execute the agent
                    await execute_func(agent, *args)
                    
                    # Save files created by this agent
                    await self._save_files_to_project(project)
                    
                    files_created = len(self.file_storage) - files_before
                    
                    # Mark agent as completed
                    session['completed_agents'].append(agent_name)
                    
                    yield {
                        'type': 'agent_completed',
                        'agent': agent_name,
                        'files_created': files_created
                    }
                    logger.info(f"[CREW] {agent_name} completed. New files: {files_created}")
                    
                except Exception as agent_error:
                    # Agent failed - store error and enable continuation
                    session['last_error'] = {
                        'agent': agent_name,
                        'error': str(agent_error),
                        'timestamp': datetime.now().isoformat()
                    }
                    session['can_continue'] = True
                    
                    logger.exception(f"[CREW] {agent_name} failed: {agent_error}")
                    
                    # Notify about failure with continuation option
                    yield {
                        'type': 'agent_failed',
                        'agent': agent_name,
                        'error': str(agent_error),
                        'can_continue': True,
                        'completed_agents': session['completed_agents']
                    }
                    
                    # Stop execution - user can continue later
                    raise
            
            # Send file tree update
            file_tree = await self._get_file_tree(project)
            yield {
                'type': 'file_tree_update',
                'tree': file_tree
            }
            
            # Pipeline complete - update session context
            session['conversation_history'].append({
                'role': 'assistant',
                'content': f'Created {len(self.file_storage)} files across all agents.',
                'files': list(self.file_storage.keys())
            })
            
            yield {
                'type': 'crew_completed',
                'total_files': len(self.file_storage),
                'message': 'Development crew completed successfully!',
                'session_executions': session['execution_count']
            }
            
            logger.info(f"[CREW] Pipeline completed. Total files: {len(self.file_storage)}")
            logger.info(f"[CREW] Session has {len(session['conversation_history'])} messages in history")
            
        except Exception as e:
            logger.exception(f"[CREW] Error executing development crew: {e}")
            
            # Check if this is a continuation-eligible error
            if session.get('can_continue'):
                yield {
                    'type': 'error',
                    'error': str(e),
                    'can_continue': True,
                    'completed_agents': session.get('completed_agents', []),
                    'failed_agent': session.get('last_error', {}).get('agent'),
                    'continuation_message': 'The pipeline can be continued from where it failed. Send another request to resume.'
                }
            else:
                yield {'type': 'error', 'error': str(e)}

    async def _execute_product_owner(
        self,
        agent,
        project: Project,
        project_description: str,
    ):
        """Execute Product Owner tasks."""
        # Create tasks
        requirements_task = create_requirements_analysis_task(
            agent,
            project_description,
            project.project_type
        )
        architecture_task = create_architecture_design_task(
            agent,
            project.project_type
        )
        
        # Create crew with sequential process and memory enabled
        crew = Crew(
            agents=[agent],
            tasks=[requirements_task, architecture_task],
            process=Process.sequential,
            verbose=self.verbose,
            memory=self.memory_enabled,
        )
        
        # Run crew (blocking operation)
        await asyncio.to_thread(crew.kickoff)
        
        logger.info("[CREW] Product Owner crew execution completed")

    async def _execute_backend_developer(
        self,
        agent,
        project: Project,
    ):
        """Execute Backend Developer tasks."""
        backend_task = create_backend_implementation_task(
            agent,
            project.project_type
        )
        api_task = create_backend_api_task(agent)
        
        crew = Crew(
            agents=[agent],
            tasks=[backend_task, api_task],
            process=Process.sequential,
            verbose=self.verbose,
            memory=self.memory_enabled,
        )
        
        await asyncio.to_thread(crew.kickoff)
        
        logger.info("[CREW] Backend Developer crew execution completed")

    async def _execute_frontend_developer(
        self,
        agent,
        project: Project,
    ):
        """Execute Frontend Developer tasks."""
        frontend_task = create_frontend_implementation_task(
            agent,
            project.project_type
        )
        integration_task = create_frontend_integration_task(agent)
        
        crew = Crew(
            agents=[agent],
            tasks=[frontend_task, integration_task],
            process=Process.sequential,
            verbose=self.verbose,
            memory=self.memory_enabled,
        )
        
        await asyncio.to_thread(crew.kickoff)
        
        logger.info("[CREW] Frontend Developer crew execution completed")

    async def _execute_qa_engineer(
        self,
        agent,
        project: Project,
    ):
        """Execute QA Engineer tasks."""
        testing_task = create_testing_task(
            agent,
            project.project_type
        )
        documentation_task = create_documentation_task(
            agent,
            project.project_type
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[testing_task, documentation_task],
            process=Process.sequential,
            verbose=self.verbose,
            memory=self.memory_enabled,
        )
        
        await asyncio.to_thread(crew.kickoff)
        
        logger.info("[CREW] QA Engineer crew execution completed")

    @database_sync_to_async
    def _save_files_to_project(self, project: Project) -> List[ProjectFile]:
        """Save files from storage to project."""
        saved_files = []
        
        for path, content in self.file_storage.items():
            # Check if file already exists in DB
            existing_file = ProjectFile.objects.filter(
                project=project,
                path=path
            ).first()
            
            if existing_file:
                # Update existing file
                existing_file.content = content
                existing_file.version += 1
                existing_file.save()
                saved_files.append(existing_file)
                logger.debug(f"[CREW] Updated file: {path}")
            else:
                # Create new file (agent tracking done separately if needed)
                file = ProjectFile.objects.create(
                    project=project,
                    path=path,
                    content=content,
                )
                saved_files.append(file)
                logger.debug(f"[CREW] Created file: {path}")
        
        return saved_files

    @database_sync_to_async
    def _get_file_tree(self, project: Project) -> Dict[str, Any]:
        """Get project file tree."""
        return project.get_file_tree()
