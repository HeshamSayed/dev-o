"""
Context Assembler

Assembles comprehensive context for agent execution.
This is the most critical component for agent collaboration.

Four-Layer Context Architecture:
1. Project Manifest (Always loaded)
2. Shared State (Real-time sync)
3. Semantic Memory (Retrieved on demand)
4. Agent Working Memory (Per-agent context)
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from django.db.models import Q
from channels.db import database_sync_to_async

from apps.agents.models import AgentInstance, AgentMessage, AgentAction
from apps.tasks.models import Task
from apps.projects.models import Project
from apps.code.models import CodeArtifact, ArtifactRegistry
from apps.context.models import Memory, Decision
from apps.llm.services.token_service import TokenCounter

logger = logging.getLogger(__name__)


@dataclass
class ContextBudget:
    """Token budget allocation for context sections"""

    system_prompt: int = 1000
    project_manifest: int = 2000
    architecture_decisions: int = 2000
    current_task: int = 1500
    relevant_code: int = 10000
    api_contracts: int = 2000
    agent_states: int = 1000
    recent_changes: int = 2000
    dependencies: int = 2000
    conversation: int = 1000
    semantic_memory: int = 2000

    @property
    def total(self) -> int:
        """Calculate total budget."""
        return sum([
            self.system_prompt,
            self.project_manifest,
            self.architecture_decisions,
            self.current_task,
            self.relevant_code,
            self.api_contracts,
            self.agent_states,
            self.recent_changes,
            self.dependencies,
            self.conversation,
            self.semantic_memory,
        ])


class ContextAssembler:
    """
    Assembles comprehensive context for agent execution.

    The context assembler is responsible for:
    1. Gathering relevant information from all sources
    2. Prioritizing information based on importance
    3. Fitting information within token budget
    4. Providing structured context to agents
    """

    def __init__(self, max_tokens: int = 28000):
        """
        Initialize context assembler.

        Args:
            max_tokens: Maximum tokens for context (default: 28K for DeepSeek-R1)
        """
        self.max_tokens = max_tokens
        self.token_counter = TokenCounter()
        self.budget = ContextBudget()

    async def assemble(
        self,
        agent: AgentInstance,
        task: Task,
        project: Project
    ) -> Dict[str, Any]:
        """
        Assemble complete context for agent execution.

        Args:
            agent: Agent instance
            task: Current task
            project: Project

        Returns:
            Context dictionary with all relevant information
        """
        context = {}
        total_tokens = 0

        # 1. Project Manifest (Layer 1 - Always loaded)
        manifest = await self._get_project_manifest(project)
        context['project_manifest'] = manifest
        total_tokens += self.token_counter.count(str(manifest))

        # 2. Current Task (High priority)
        task_context = await self._get_task_context(task)
        task_prompt = await self._format_task_prompt(task)
        context['current_task_data'] = task_context
        context['current_task_prompt'] = task_prompt
        total_tokens += self.token_counter.count(task_prompt)

        # 3. Architecture Decisions (Layer 1)
        decisions = await self._get_relevant_decisions(project, task)
        context['architecture_decisions'] = decisions
        total_tokens += self.token_counter.count(str(decisions))

        # 4. API Contracts (Layer 1)
        api_contracts = await self._get_api_contracts(project, task)
        context['api_contracts'] = api_contracts
        total_tokens += self.token_counter.count(str(api_contracts))

        # 5. Relevant Code (Layer 3 - Semantic search)
        remaining_for_code = self.budget.relevant_code
        relevant_code = await self._get_relevant_code(project, task, remaining_for_code)
        context['relevant_code'] = relevant_code
        total_tokens += self.token_counter.count(str(relevant_code))

        # 6. Agent States (Layer 2 - Real-time)
        agent_states = await self._get_agent_states(project, agent)
        context['agent_states'] = agent_states
        total_tokens += self.token_counter.count(str(agent_states))

        # 7. Team Agents (if any hired by this agent)
        team_agents = await self._get_team_agents(agent)
        context['team_agents'] = team_agents
        total_tokens += self.token_counter.count(str(team_agents))

        # 8. Recent Changes (Layer 2)
        recent_changes = await self._get_recent_changes(project)
        context['recent_changes'] = recent_changes
        total_tokens += self.token_counter.count(str(recent_changes))

        # 9. Dependencies (Layer 2)
        dependencies = await self._get_task_dependencies(task)
        context['dependencies'] = dependencies
        total_tokens += self.token_counter.count(str(dependencies))

        # 10. Conversation History (Layer 4)
        conversation = await self._get_conversation_history(agent)
        context['user_history'] = conversation
        total_tokens += self.token_counter.count(str(conversation))

        # 11. Semantic Memory (Layer 3 - if budget allows)
        remaining = self.max_tokens - total_tokens
        if remaining > 500:
            memories = await self._retrieve_memories(project, task, remaining)
            context['semantic_memory'] = memories
            total_tokens += self.token_counter.count(str(memories))

        # Add metadata
        context['token_count'] = total_tokens
        context['max_tokens'] = self.max_tokens

        @database_sync_to_async
        def get_tech_stack():
            return project.manifest.get('tech_stack', {}) if project.manifest else {}

        tech_stack = await get_tech_stack()
        context['tech_stack'] = tech_stack

        @database_sync_to_async
        def get_agent_name():
            return agent.agent_type.name

        agent_name = await get_agent_name()
        logger.info(f"Context assembled: {total_tokens} tokens for agent {agent_name}")

        return context

    async def _get_project_manifest(self, project: Project) -> Dict[str, Any]:
        """Get structured project manifest (Layer 1)."""
        @database_sync_to_async
        def get_manifest():
            manifest = project.manifest or {}

            return {
                "name": project.name,
                "description": project.description,
                "status": project.status,
                "requirements": manifest.get("requirements", {}),
                "domain_model": manifest.get("domain_model", {}),
                "tech_stack": manifest.get("tech_stack", {}),
                "architecture": manifest.get("architecture", {}),
            }

        return await get_manifest()

    async def _get_task_context(self, task: Task) -> Dict[str, Any]:
        """Get current task details."""
        @database_sync_to_async
        def get_context():
            return {
                "id": str(task.id),
                "title": task.title,
                "type": task.task_type,
                "priority": task.priority,
                "status": task.status,
                "description": task.description,
                "requirements": task.requirements,
                "acceptance_criteria": task.acceptance_criteria,
                "deliverables": task.deliverables,
                "iteration": task.iteration_count,
                "parent_task": str(task.parent_task_id) if task.parent_task_id else None,
            }

        return await get_context()

    async def _format_task_prompt(self, task: Task) -> str:
        """Format task as a prompt for the agent."""
        @database_sync_to_async
        def format_prompt():
            prompt = f"""## Your Current Task

**{task.title}**

Type: {task.task_type}
Priority: {task.get_priority_display()}
Status: {task.get_status_display()}

### Description
{task.description}
"""

            # Add requirements
            if task.requirements:
                prompt += "\n### Requirements\n"
                for key, value in task.requirements.items():
                    if isinstance(value, list):
                        prompt += f"\n**{key}:**\n"
                        for item in value:
                            prompt += f"- {item}\n"
                    else:
                        prompt += f"- **{key}:** {value}\n"

            # Add acceptance criteria
            if task.acceptance_criteria:
                prompt += "\n### Acceptance Criteria\n"
                for criterion in task.acceptance_criteria:
                    prompt += f"- [ ] {criterion}\n"

            # Add deliverables
            if task.deliverables:
                prompt += "\n### Expected Deliverables\n"
                for deliverable in task.deliverables:
                    prompt += f"- {deliverable}\n"

            return prompt

        return await format_prompt()

    async def _get_relevant_decisions(
        self,
        project: Project,
        task: Task
    ) -> List[Dict[str, Any]]:
        """Get architecture decisions relevant to the task."""
        @database_sync_to_async
        def get_decisions():
            decisions = Decision.objects.filter(
                project=project,
                status__in=['approved', 'implemented']
            ).order_by('-created_at')[:10]

            return [
                {
                    "id": str(d.id),
                    "type": d.decision_type,
                    "title": d.title,
                    "description": d.description,
                    "reasoning": d.reasoning,
                    "affected_components": d.affected_components,
                }
                for d in decisions
            ]

        return await get_decisions()

    async def _get_api_contracts(
        self,
        project: Project,
        task: Task
    ) -> List[Dict[str, Any]]:
        """Get relevant API contracts from artifact registry."""
        @database_sync_to_async
        def get_contracts():
            contracts = ArtifactRegistry.objects.filter(
                project=project,
                artifact_type='api_endpoint',
                is_active=True
            )[:20]

            return [
                {
                    "name": c.name,
                    "file_path": c.file_path,
                    "details": c.details
                }
                for c in contracts
            ]

        return await get_contracts()

    async def _get_relevant_code(
        self,
        project: Project,
        task: Task,
        max_tokens: int
    ) -> List[Dict[str, Any]]:
        """Get code files relevant to the task."""
        # For now, get recently modified files
        # TODO: Implement semantic search with embeddings
        @database_sync_to_async
        def get_artifacts():
            return list(CodeArtifact.objects.filter(
                project=project
            ).order_by('-updated_at')[:10])

        artifacts = await get_artifacts()
        result = []
        tokens_used = 0

        for artifact in artifacts:
            artifact_tokens = self.token_counter.count(artifact.content)

            if tokens_used + artifact_tokens > max_tokens:
                # Try to include truncated version
                if tokens_used + 500 < max_tokens:
                    truncated = self._truncate_code(
                        artifact.content,
                        max_tokens - tokens_used - 100
                    )
                    result.append({
                        "path": artifact.file_path,
                        "language": artifact.language,
                        "content": truncated,
                        "truncated": True,
                        "structure": artifact.structure
                    })
                break

            result.append({
                "path": artifact.file_path,
                "language": artifact.language,
                "content": artifact.content,
                "truncated": False,
                "structure": artifact.structure
            })
            tokens_used += artifact_tokens

        return result

    def _truncate_code(self, content: str, max_tokens: int) -> str:
        """Truncate code while keeping important parts."""
        lines = content.split('\n')

        # Keep imports, class/function definitions
        important_lines = []
        for i, line in enumerate(lines):
            stripped = line.strip()
            if (
                stripped.startswith('import ') or
                stripped.startswith('from ') or
                stripped.startswith('class ') or
                stripped.startswith('def ') or
                stripped.startswith('async def ') or
                stripped.startswith('@')
            ):
                important_lines.append((i, line))

        # Build truncated version
        result_lines = []
        current_tokens = 0

        for idx, line in important_lines:
            line_tokens = self.token_counter.count(line)
            if current_tokens + line_tokens > max_tokens:
                break
            result_lines.append(line)
            current_tokens += line_tokens

        return '\n'.join(result_lines) + '\n\n# ... (truncated)'

    async def _get_agent_states(
        self,
        project: Project,
        current_agent: AgentInstance
    ) -> List[Dict[str, Any]]:
        """Get status of all agents in the project (Layer 2)."""
        @database_sync_to_async
        def get_agents():
            agents = AgentInstance.objects.filter(
                project=project
            ).exclude(
                id=current_agent.id
            ).select_related('agent_type', 'current_task')

            return [
                {
                    "id": str(a.id),
                    "type": a.agent_type.name,
                    "role": a.agent_type.role,
                    "status": a.status,
                    "current_task": a.current_task.title if a.current_task else None,
                    "last_active": a.last_active_at.isoformat() if a.last_active_at else None
                }
                for a in agents
            ]

        return await get_agents()

    async def _get_team_agents(self, agent: AgentInstance) -> List[Dict[str, Any]]:
        """Get agents hired by this agent."""
        @database_sync_to_async
        def get_hired():
            hired = agent.hired_agents.all().select_related('agent_type', 'current_task')

            return [
                {
                    "id": str(a.id),
                    "type": a.agent_type.name,
                    "status": a.status,
                    "current_task": a.current_task.title if a.current_task else None
                }
                for a in hired
            ]

        return await get_hired()

    async def _get_recent_changes(self, project: Project) -> List[Dict[str, Any]]:
        """Get recent changes in the project (Layer 2)."""
        from datetime import timedelta
        from django.utils import timezone

        @database_sync_to_async
        def get_actions():
            one_hour_ago = timezone.now() - timedelta(hours=1)

            actions = AgentAction.objects.filter(
                project=project,
                created_at__gte=one_hour_ago
            ).select_related('agent', 'agent__agent_type').order_by('-created_at')[:20]

            return [
                {
                    "type": a.action_type,
                    "agent": a.agent.agent_type.name,
                    "data": a.action_data,
                    "timestamp": a.created_at.isoformat()
                }
                for a in actions
            ]

        return await get_actions()

    async def _get_task_dependencies(self, task: Task) -> Dict[str, Any]:
        """Get dependencies and their outputs."""
        @database_sync_to_async
        def get_deps():
            deps = task.dependencies.select_related('depends_on').all()

            result = {
                "blocking": [],
                "outputs": []
            }

            for dep in deps:
                dep_task = dep.depends_on
                dep_info = {
                    "task_id": str(dep_task.id),
                    "title": dep_task.title,
                    "status": dep_task.status,
                    "type": dep.dependency_type
                }

                if dep_task.status == 'completed':
                    # Include outputs
                    dep_info["deliverables"] = dep_task.deliverables
                    dep_info["summary"] = dep_task.completion_summary
                    result["outputs"].append(dep_info)
                else:
                    result["blocking"].append(dep_info)

            return result

        return await get_deps()

    async def _get_conversation_history(
        self,
        agent: AgentInstance,
        max_messages: int = 20
    ) -> List[Dict[str, str]]:
        """Get agent's conversation history (Layer 4)."""
        @database_sync_to_async
        def get_history():
            return agent.conversation_history[-max_messages:] if agent.conversation_history else []

        return await get_history()

    async def _retrieve_memories(
        self,
        project: Project,
        task: Task,
        max_tokens: int
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant memories via semantic search (Layer 3)."""
        # For now, get recent memories
        # TODO: Implement semantic search with embeddings
        @database_sync_to_async
        def get_memories():
            memories = Memory.objects.filter(
                project=project
            ).order_by('-importance', '-created_at')[:10]

            result = []
            tokens_used = 0

            for memory in memories:
                memory_tokens = self.token_counter.count(memory.content)
                if tokens_used + memory_tokens > max_tokens:
                    break

                result.append({
                    "type": memory.memory_type,
                    "title": memory.title,
                    "content": memory.content[:1000],  # Truncate individual memories
                })
                tokens_used += memory_tokens

                # Update access count
                memory.access_count += 1
                memory.save(update_fields=['access_count'])

            return result

        return await get_memories()
