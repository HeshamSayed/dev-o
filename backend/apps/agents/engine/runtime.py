"""
Agent Runtime

Main runtime for executing agents with state machine and tool execution.
"""

import logging
import asyncio
from typing import Dict, Any, AsyncGenerator, Optional
from datetime import datetime
from channels.db import database_sync_to_async

from apps.agents.models import AgentInstance, AgentStatus, AgentAction
from apps.tasks.models import Task, TaskStatus
from apps.llm.services.llm_service import LLMService
from apps.llm.clients.base import LLMResponse
from apps.context.services.context_assembler import ContextAssembler
from apps.agents.types.base import ToolCall
from apps.agents.tools import get_tool

logger = logging.getLogger(__name__)


class AgentRuntime:
    """
    Agent execution runtime.

    Manages:
    - Agent state transitions
    - LLM interaction
    - Tool execution
    - Context assembly
    - Error recovery
    - Checkpointing
    """

    def __init__(
        self,
        agent: AgentInstance,
        agent_type_handler: Any,  # BaseAgentType instance
        llm_service: Optional[LLMService] = None
    ):
        """
        Initialize agent runtime.

        Args:
            agent: Agent instance to execute
            agent_type_handler: Agent type handler (orchestrator, architect, etc.)
            llm_service: LLM service (creates if not provided)
        """
        self.agent = agent
        self.agent_type_handler = agent_type_handler
        self.llm_service = llm_service or LLMService(model=agent.model)
        # Use maximum context for better quality results
        self.context_assembler = ContextAssembler(max_tokens=16000)

        self.iteration = 0
        self.max_iterations = agent_type_handler.persona.max_iterations
        self.is_cancelled = False

    async def execute_task(
        self,
        task: Task,
        stream: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute a task with this agent.

        Args:
            task: Task to execute
            stream: Whether to stream events

        Yields:
            Event dictionaries for real-time updates
        """
        try:
            # Update agent status
            await self._update_agent_status(AgentStatus.WORKING, task)

            @database_sync_to_async
            def get_agent_info():
                return self.agent.agent_type.name, task.title

            agent_name, task_title = await get_agent_info()

            yield {
                "type": "agent_start",
                "agent": agent_name,
                "task": task_title,
                "timestamp": datetime.now().isoformat()
            }

            # Execute main loop
            async for event in self._execution_loop(task, stream):
                yield event

                # Check for cancellation
                if self.is_cancelled:
                    yield {
                        "type": "cancelled",
                        "message": "Execution cancelled by user",
                        "timestamp": datetime.now().isoformat()
                    }
                    break

        except Exception as e:
            logger.exception(f"Error in agent execution: {e}")
            yield {
                "type": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            await self._update_agent_status(AgentStatus.ERROR)
            raise

        finally:
            # Save final state
            await self._save_checkpoint()

    async def _execution_loop(
        self,
        task: Task,
        stream: bool
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Main execution loop with state machine."""

        while self.iteration < self.max_iterations:
            self.iteration += 1

            yield {
                "type": "iteration_start",
                "iteration": self.iteration,
                "max_iterations": self.max_iterations,
                "timestamp": datetime.now().isoformat()
            }

            # 1. Assemble context
            context = await self._assemble_context(task)

            yield {
                "type": "context_assembled",
                "token_count": context.get("token_count", 0),
                "timestamp": datetime.now().isoformat()
            }

            # 2. Generate system prompt
            system_prompt = self.agent_type_handler.get_system_prompt(context)

            # 3. Call LLM with streaming
            response = None
            if stream:
                # Stream LLM response in real-time
                async for event in self._call_llm_stream(system_prompt, context):
                    if 'response' in event:
                        # This is the final parsed response
                        response = event['response']
                    else:
                        # This is a streaming event, forward it
                        yield event
            else:
                response = await self._call_llm(system_prompt, context, stream)

                # Yield thinking (for R1 models)
                if response.thinking:
                    yield {
                        "type": "thinking",
                        "content": response.thinking,
                        "timestamp": datetime.now().isoformat()
                    }

                # 4. Yield agent message
                if response.content:
                    yield {
                        "type": "content",
                        "content": response.content,
                        "timestamp": datetime.now().isoformat()
                    }

            # Ensure we have a response
            if not response:
                raise RuntimeError("No response received from LLM")

            # 5. Check for final answer
            if response.is_final and not response.tool_calls:
                yield {
                    "type": "final_response",
                    "content": response.content,
                    "timestamp": datetime.now().isoformat()
                }

                # Complete the task
                await self._complete_task(task, response)

                yield {
                    "type": "task_completed",
                    "task_id": str(task.id),
                    "summary": response.content[:500],
                    "timestamp": datetime.now().isoformat()
                }
                return

            # 6. Handle user input request
            if response.needs_user_input:
                yield {
                    "type": "user_input_required",
                    "question": response.user_question,
                    "timestamp": datetime.now().isoformat()
                }

                await self._update_agent_status(AgentStatus.WAITING_INPUT)
                return

            # 7. Handle blocker
            if response.is_blocked:
                yield {
                    "type": "blocked",
                    "description": response.blocker_description,
                    "timestamp": datetime.now().isoformat()
                }

                await self._handle_blocker(task, response.blocker_description)
                return

            # 8. Execute tool calls
            if response.tool_calls:
                for tool_call_data in response.tool_calls:
                    tool_call = ToolCall(
                        tool_name=tool_call_data.get('tool', ''),
                        arguments=tool_call_data.get('arguments', {}),
                        reasoning=tool_call_data.get('reasoning', '')
                    )

                    yield {
                        "type": "tool_call_start",
                        "tool": tool_call.tool_name,
                        "arguments": tool_call.arguments,
                        "reasoning": tool_call.reasoning,
                        "timestamp": datetime.now().isoformat()
                    }

                    result = await self._execute_tool(tool_call, task)

                    yield {
                        "type": "tool_call_result",
                        "tool": tool_call.tool_name,
                        "success": result.get("success", False),
                        "result": result.get("message", ""),
                        "timestamp": datetime.now().isoformat()
                    }

                    # Add result to working memory
                    await self._update_working_memory(tool_call, result)

            # Small delay to prevent tight loops
            await asyncio.sleep(0.1)

        # Max iterations reached
        yield {
            "type": "max_iterations",
            "message": f"Reached maximum iterations ({self.max_iterations})",
            "timestamp": datetime.now().isoformat()
        }

        await self._update_agent_status(AgentStatus.BLOCKED)

    async def _assemble_context(self, task: Task) -> Dict[str, Any]:
        """Assemble context for the agent."""
        @database_sync_to_async
        def get_project():
            return self.agent.project

        project = await get_project()
        return await self.context_assembler.assemble(
            agent=self.agent,
            task=task,
            project=project
        )

    async def _call_llm(
        self,
        system_prompt: str,
        context: Dict[str, Any],
        stream: bool
    ) -> LLMResponse:
        """Call the LLM and parse response."""

        # Build current task prompt
        task_prompt = context.get('current_task_prompt', '')

        # Get tool definitions
        tools = self.agent_type_handler.get_tool_definitions()

        # Get agent temperature
        @database_sync_to_async
        def get_temperature():
            return self.agent.temperature

        temperature = await get_temperature()

        # Call LLM (returns already-parsed LLMResponse)
        response = await self.llm_service.generate(
            prompt=task_prompt,
            system=system_prompt,
            messages=context.get('user_history', []),
            temperature=temperature,
            tools=tools
        )

        # Response is already parsed
        return response

    async def _call_llm_stream(
        self,
        system_prompt: str,
        context: Dict[str, Any]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Call the LLM with streaming and yield chunks in real-time."""

        try:
            # Build current task prompt
            task_prompt = context.get('current_task_prompt', '')
            logger.info(f"[LLM] Starting streaming call with prompt length: {len(task_prompt)}")

            # Get tool definitions
            tools = self.agent_type_handler.get_tool_definitions()

            # Get agent temperature
            @database_sync_to_async
            def get_temperature():
                return self.agent.temperature

            temperature = await get_temperature()
            logger.info(f"[LLM] Temperature: {temperature}, Tools: {len(tools) if tools else 0}")

            # Stream LLM response - buffer all chunks first, then parse and stream clean text
            response_chunks = []
            chunk_count = 0
            async for chunk in self.llm_service.generate_stream(
                prompt=task_prompt,
                system=system_prompt,
                messages=context.get('user_history', []),
                temperature=temperature,
                tools=tools
            ):
                chunk_count += 1
                response_chunks.append(chunk)

            logger.info(f"[LLM] Streaming complete. Received {chunk_count} chunks")

        except Exception as e:
            logger.exception(f"[LLM] Error in streaming: {e}")
            raise

        # Parse the full response - efficient string join
        full_response = "".join(response_chunks)
        response = self.llm_service.client.parse_response(full_response)

        # Stream the CLEAN conversational content (with tool calls removed)
        if response.content:
            # Stream word by word for natural effect
            words = response.content.split()
            for i, word in enumerate(words):
                # Add space except for first word
                chunk_text = word if i == 0 else f" {word}"
                yield {
                    "type": "content_chunk",
                    "chunk": chunk_text,
                    "timestamp": datetime.now().isoformat()
                }
                # Small delay for natural streaming effect
                await asyncio.sleep(0.01)

        # Yield thinking if present (R1 models)
        if response.thinking:
            yield {
                "type": "thinking",
                "content": response.thinking,
                "timestamp": datetime.now().isoformat()
            }

        # Return parsed response as a special event
        yield {
            "type": "stream_complete",
            "response": response,
            "timestamp": datetime.now().isoformat()
        }

    async def _execute_tool(
        self,
        tool_call: ToolCall,
        task: Task
    ) -> Dict[str, Any]:
        """
        Execute a tool call.

        Args:
            tool_call: Tool call information
            task: Current task

        Returns:
            Tool result dictionary
        """
        logger.info(f"Executing tool: {tool_call.tool_name} with args: {tool_call.arguments}")

        # Get tool from registry
        tool = get_tool(tool_call.tool_name)

        if not tool:
            logger.error(f"Tool not found: {tool_call.tool_name}")
            return {
                "success": False,
                "message": f"Unknown tool: {tool_call.tool_name}",
                "error_code": "TOOL_NOT_FOUND"
            }

        # Build execution context
        @database_sync_to_async
        def get_project():
            return self.agent.project

        project = await get_project()
        context = {
            "agent": self.agent,
            "task": task,
            "project": project
        }

        try:
            # Execute tool
            result = await tool.execute(tool_call.arguments, context)

            # Log action for event sourcing
            await self._log_action(tool_call, result.to_dict(), task)

            return result.to_dict()

        except Exception as e:
            logger.exception(f"Error executing tool {tool_call.tool_name}: {e}")
            return {
                "success": False,
                "message": f"Tool execution failed: {str(e)}",
                "error_code": "EXECUTION_ERROR"
            }

    async def _log_action(
        self,
        tool_call: ToolCall,
        result: Dict[str, Any],
        task: Task
    ):
        """Log agent action for event sourcing."""
        @database_sync_to_async
        def create_action():
            return AgentAction.objects.create(
                project=self.agent.project,
                agent=self.agent,
                task=task,
                action_type=f"tool_{tool_call.tool_name}",
                action_data={
                    "tool": tool_call.tool_name,
                    "arguments": tool_call.arguments,
                    "reasoning": tool_call.reasoning,
                    "result": result
                },
                is_reversible=result.get("is_reversible", False),
                reverse_action=result.get("reverse_action")
            )

        await create_action()

    async def _update_working_memory(
        self,
        tool_call: ToolCall,
        result: Dict[str, Any]
    ):
        """Update agent's working memory with tool result."""
        memory = self.agent.working_memory or {}

        # Track tool calls
        if "tool_calls" not in memory:
            memory["tool_calls"] = []

        memory["tool_calls"].append({
            "tool": tool_call.tool_name,
            "arguments": tool_call.arguments,
            "result_summary": str(result)[:200],
            "timestamp": datetime.now().isoformat()
        })

        # Keep last 20 tool calls
        memory["tool_calls"] = memory["tool_calls"][-20:]

        self.agent.working_memory = memory
        await database_sync_to_async(self.agent.save)(update_fields=["working_memory"])

    async def _update_agent_status(
        self,
        status: AgentStatus,
        task: Optional[Task] = None
    ):
        """Update agent status."""
        self.agent.status = status
        if task:
            self.agent.current_task = task
        self.agent.last_active_at = datetime.now()
        await database_sync_to_async(self.agent.save)()

    async def _complete_task(self, task: Task, response: LLMResponse):
        """Mark task as completed."""
        task.status = TaskStatus.COMPLETED
        task.completion_summary = response.content
        task.completed_at = datetime.now()
        if response.files_created or response.files_modified:
            task.deliverables = response.files_created + response.files_modified
        await database_sync_to_async(task.save)()

        # Update agent stats
        self.agent.tasks_completed += 1
        self.agent.status = AgentStatus.IDLE
        self.agent.current_task = None
        await database_sync_to_async(self.agent.save)()

    async def _handle_blocker(self, task: Task, description: str):
        """Handle a blocked task."""
        task.status = TaskStatus.BLOCKED
        await database_sync_to_async(task.save)()

        self.agent.status = AgentStatus.BLOCKED
        self.agent.status_message = description
        await database_sync_to_async(self.agent.save)()

        # TODO: Notify supervisor agent
        @database_sync_to_async
        def get_agent_name():
            return self.agent.agent_type.name

        agent_name = await get_agent_name()
        logger.warning(f"Agent {agent_name} blocked: {description}")

    async def _save_checkpoint(self):
        """Save execution checkpoint."""
        from apps.projects.models import ProjectCheckpoint

        @database_sync_to_async
        def create_checkpoint():
            return ProjectCheckpoint.objects.create(
                project=self.agent.project,
                name=f"Auto checkpoint - {datetime.now().isoformat()}",
                state_snapshot={
                    "agent_id": str(self.agent.id),
                    "iteration": self.iteration,
                    "working_memory": self.agent.working_memory,
                    "conversation_history": self.agent.conversation_history
                },
                created_by=str(self.agent.id),
                is_auto=True
            )

        await create_checkpoint()

    def cancel(self):
        """Cancel execution."""
        self.is_cancelled = True
        logger.info(f"Agent {self.agent.agent_type.name} execution cancelled")
