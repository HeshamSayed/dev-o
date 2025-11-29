"""
Conversation Orchestrator

Manages multi-agent conversations where agents discuss in real-time,
share context, and users can participate.

NO TOOL EXECUTION - Pure conversation mode.
"""

import logging
import asyncio
from typing import Dict, Any, List, AsyncGenerator, Optional
from dataclasses import dataclass
from datetime import datetime
from channels.db import database_sync_to_async

from apps.agents.models import AgentInstance
from apps.projects.models import Project
from apps.llm.services.llm_service import LLMService

logger = logging.getLogger(__name__)


@dataclass
class ConversationMessage:
    """A message in the conversation."""
    speaker: str  # "user", "Alex", "Sarah", "Marcus", "Elena"
    content: str
    timestamp: datetime
    role: str  # "user", "orchestrator", "architect", "backend_lead", "frontend_lead"


class ConversationOrchestrator:
    """
    Orchestrates multi-agent conversations.

    Flow:
    1. User sends message
    2. Alex (Orchestrator) responds and gathers requirements
    3. Alex brings in Sarah (Architect) when needed
    4. Agents can ask each other questions
    5. User can interrupt and participate
    6. Leads (Marcus, Elena) join to assess work

    Features:
    - Shared conversation context (all agents see all messages)
    - Turn-taking to prevent infinite loops
    - Real-time streaming
    - User can interrupt anytime
    """

    def __init__(self, project: Project):
        self.project = project
        self.conversation_history: List[ConversationMessage] = []
        self.active_agents: Dict[str, AgentInstance] = {}
        self.llm_services: Dict[str, LLMService] = {}

        # Turn management
        self.max_turns_per_agent = 3  # Max consecutive turns before passing
        self.max_total_turns = 20  # Max total turns to prevent infinite loops
        self.current_turn_count = 0
        self.agent_turn_counts: Dict[str, int] = {}

    async def initialize_agents(self):
        """Initialize all agents for the project."""
        @database_sync_to_async
        def get_agents():
            from apps.agents.models import AgentType
            agents = {}

            # Get or create Alex (Orchestrator)
            orchestrator_type = AgentType.objects.filter(role='orchestrator').first()
            if orchestrator_type:
                alex, _ = AgentInstance.objects.get_or_create(
                    project=self.project,
                    agent_type=orchestrator_type,
                    defaults={'status': 'idle'}
                )
                agents['Alex'] = alex

            # Get or create Sarah (Architect)
            architect_type = AgentType.objects.filter(role='architect').first()
            if architect_type:
                sarah, _ = AgentInstance.objects.get_or_create(
                    project=self.project,
                    agent_type=architect_type,
                    defaults={'status': 'idle'}
                )
                agents['Sarah'] = sarah

            # Get or create Marcus (Backend Lead)
            backend_type = AgentType.objects.filter(role='backend_lead').first()
            if backend_type:
                marcus, _ = AgentInstance.objects.get_or_create(
                    project=self.project,
                    agent_type=backend_type,
                    defaults={'status': 'idle'}
                )
                agents['Marcus'] = marcus

            # Get or create Elena (Frontend Lead)
            frontend_type = AgentType.objects.filter(role='frontend_lead').first()
            if frontend_type:
                elena, _ = AgentInstance.objects.get_or_create(
                    project=self.project,
                    agent_type=frontend_type,
                    defaults={'status': 'idle'}
                )
                agents['Elena'] = elena

            return agents

        self.active_agents = await get_agents()

        # Initialize LLM services for each agent
        for name, agent in self.active_agents.items():
            @database_sync_to_async
            def get_model():
                return agent.model

            model = await get_model()
            self.llm_services[name] = LLMService(model=model)

        logger.info(f"Initialized {len(self.active_agents)} agents: {list(self.active_agents.keys())}")

    def add_message(self, speaker: str, content: str, role: str = "user"):
        """Add a message to the conversation history."""
        message = ConversationMessage(
            speaker=speaker,
            content=content,
            timestamp=datetime.now(),
            role=role
        )
        self.conversation_history.append(message)
        logger.info(f"[Conversation] {speaker}: {content[:100]}...")

    def get_conversation_context(self, for_agent: str) -> str:
        """Build conversation context string for an agent."""
        context_lines = []
        context_lines.append("=== CONVERSATION HISTORY ===\n")

        for msg in self.conversation_history[-10:]:  # Last 10 messages
            context_lines.append(f"{msg.speaker}: {msg.content}")

        context_lines.append(f"\n=== YOUR TURN ({for_agent}) ===")
        return "\n".join(context_lines)

    def should_bring_in_architect(self) -> bool:
        """Determine if we should bring in the architect."""
        # Bring in architect after Alex gathers initial requirements
        alex_messages = [m for m in self.conversation_history if m.speaker == "Alex"]
        sarah_messages = [m for m in self.conversation_history if m.speaker == "Sarah"]

        # If Alex has spoken 2+ times and Sarah hasn't joined, bring her in
        return len(alex_messages) >= 2 and len(sarah_messages) == 0

    def should_bring_in_leads(self) -> bool:
        """Determine if we should bring in technical leads."""
        # Bring in leads after architect has done initial design
        sarah_messages = [m for m in self.conversation_history if m.speaker == "Sarah"]
        marcus_messages = [m for m in self.conversation_history if m.speaker == "Marcus"]
        elena_messages = [m for m in self.conversation_history if m.speaker == "Elena"]

        # If Sarah has spoken 2+ times and leads haven't joined, bring them in
        return len(sarah_messages) >= 2 and len(marcus_messages) == 0 and len(elena_messages) == 0

    def get_next_speaker(self) -> Optional[str]:
        """Determine who should speak next."""
        # Prevent infinite loops
        if self.current_turn_count >= self.max_total_turns:
            logger.warning("Max total turns reached, ending conversation")
            return None

        # Always start with Alex
        if len(self.conversation_history) <= 1:
            return "Alex"

        last_speaker = self.conversation_history[-1].speaker if self.conversation_history else None
        last_message = self.conversation_history[-1].content if self.conversation_history else ""

        # Check if last speaker has exceeded consecutive turns
        if last_speaker and last_speaker != "User":
            self.agent_turn_counts[last_speaker] = self.agent_turn_counts.get(last_speaker, 0) + 1

            if self.agent_turn_counts[last_speaker] >= self.max_turns_per_agent:
                # Reset count and pass to someone else
                self.agent_turn_counts[last_speaker] = 0
                logger.info(f"{last_speaker} exceeded max turns, passing to others")

        # Determine next speaker based on conversation flow
        if last_speaker == "User" or last_speaker is None:
            return "Alex"  # Alex always responds to user

        elif last_speaker == "Alex":
            # Check if Alex is delegating/hiring someone
            if "[HIRE Sarah]" in last_message or "[HIRE SARAH]" in last_message.upper():
                return "Sarah"  # Sarah should respond after being hired
            elif "[HIRE Marcus]" in last_message or "[HIRE MARCUS]" in last_message.upper() or "Marcus - Backend" in last_message:
                return "Marcus"  # Marcus should respond after being hired
            elif "[HIRE Elena]" in last_message or "[HIRE ELENA]" in last_message.upper() or "Elena - Frontend" in last_message:
                return "Elena"  # Elena should respond after being hired
            elif self.should_bring_in_architect():
                return "Sarah"  # Bring in architect
            else:
                return None  # Wait for user input

        elif last_speaker == "Sarah":
            # If Sarah just provided architecture/design, let Alex respond
            if "```" in last_message or "schema" in last_message.lower() or "architecture" in last_message.lower():
                # Check if this is her first substantial contribution
                sarah_messages = [m for m in self.conversation_history if m.speaker == "Sarah"]
                if len(sarah_messages) <= 2:
                    return "Alex"  # Let Alex acknowledge and continue

            if self.should_bring_in_leads():
                # Randomly choose between Marcus and Elena
                import random
                return random.choice(["Marcus", "Elena"])
            else:
                # Sarah can ask Alex for clarification
                if "question" in last_message.lower() or "?" in last_message:
                    return "Alex"
                else:
                    return None  # Wait for user input

        elif last_speaker in ["Marcus", "Elena"]:
            # If lead just provided code, let Alex respond
            if "```" in last_message:
                # Check if this is their first substantial contribution
                lead_messages = [m for m in self.conversation_history if m.speaker == last_speaker]
                if len(lead_messages) <= 2:
                    return "Alex"  # Let Alex acknowledge

            # Leads can respond to each other or wait for user
            other_lead = "Elena" if last_speaker == "Marcus" else "Marcus"
            other_lead_messages = [m for m in self.conversation_history if m.speaker == other_lead]

            if len(other_lead_messages) == 0:
                return other_lead  # Let other lead speak
            else:
                return None  # Wait for user input

        return None

    async def process_user_message(
        self,
        user_message: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process a user message and orchestrate agent responses.

        Yields events for the WebSocket stream.
        """
        # Add user message to history
        self.add_message("User", user_message, "user")

        # Yield user message event
        yield {
            "type": "message",
            "speaker": "User",
            "content": user_message,
            "role": "user",
            "timestamp": datetime.now().isoformat()
        }

        # Continue conversation until no one wants to speak
        while True:
            next_speaker = self.get_next_speaker()

            if next_speaker is None:
                # No one wants to speak, wait for user input
                yield {
                    "type": "waiting_for_user",
                    "message": "Agents are waiting for your input",
                    "timestamp": datetime.now().isoformat()
                }
                break

            # Generate response from next speaker
            async for event in self._generate_agent_response(next_speaker):
                yield event

            self.current_turn_count += 1

            # Small delay between agent responses for natural flow
            await asyncio.sleep(0.5)

    async def _generate_agent_response(
        self,
        agent_name: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Generate a response from a specific agent."""
        if agent_name not in self.active_agents:
            logger.error(f"Agent {agent_name} not found")
            return

        agent = self.active_agents[agent_name]
        llm_service = self.llm_services[agent_name]

        # Build conversation context
        conversation_context = self.get_conversation_context(agent_name)

        # Get agent's system prompt
        system_prompt = await self._get_agent_system_prompt(agent_name)

        # Yield thinking event
        yield {
            "type": "agent_thinking",
            "speaker": agent_name,
            "timestamp": datetime.now().isoformat()
        }

        # Stream response word by word
        full_response = ""
        word_buffer = []

        try:
            async for chunk in llm_service.generate_stream(
                prompt=conversation_context,
                system=system_prompt,
                temperature=0.8,
                max_tokens=16000
            ):
                full_response += chunk
                word_buffer.append(chunk)

                # Stream every few words for natural effect
                if len(word_buffer) >= 3 or chunk in ['.', '?', '!', '\n']:
                    text = ''.join(word_buffer)
                    yield {
                        "type": "message_chunk",
                        "speaker": agent_name,
                        "chunk": text,
                        "timestamp": datetime.now().isoformat()
                    }
                    word_buffer = []
                    await asyncio.sleep(0.05)  # Natural typing speed

            # Flush remaining buffer
            if word_buffer:
                text = ''.join(word_buffer)
                yield {
                    "type": "message_chunk",
                    "speaker": agent_name,
                    "chunk": text,
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            logger.exception(f"Error generating response for {agent_name}: {e}")
            yield {
                "type": "error",
                "speaker": agent_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            return

        # Add to conversation history
        @database_sync_to_async
        def get_agent_role():
            return agent.agent_type.role

        role = await get_agent_role()
        self.add_message(agent_name, full_response, role)

        # Yield message complete event
        yield {
            "type": "message_complete",
            "speaker": agent_name,
            "content": full_response,
            "role": role,
            "timestamp": datetime.now().isoformat()
        }

    async def _get_agent_system_prompt(self, agent_name: str) -> str:
        """Get conversation-mode system prompt for an agent."""
        # Get the full persona prompt from the agent type
        if agent_name not in self.active_agents:
            return "You are a helpful team member."

        @database_sync_to_async
        def get_agent_prompt():
            agent = self.active_agents[agent_name]
            return agent.agent_type.system_prompt

        full_prompt = await get_agent_prompt()

        # Add conversation context note to the full prompt
        conversation_note = f"""

=== CONVERSATION MODE ===
You are currently in a team conversation with the user and other team members.
All messages are visible to everyone in the conversation.

**CRITICAL**: When you're hired or asked to do something, you must IMMEDIATELY provide the deliverable in the chat:
- If asked for architecture → Provide the full architecture document with code examples in markdown
- If asked for database schema → Provide the complete SQL schema in code blocks
- If asked for API code → Provide the complete FastAPI/backend code in code blocks
- If asked for frontend code → Provide the complete component code in code blocks

DO NOT just say "I'll do it" or "I'm working on it" - ACTUALLY PROVIDE THE CODE/DESIGN IN THIS MESSAGE.

Use proper markdown code blocks with language tags:
```python
# Your code here
```

```sql
-- Your SQL here
```

Current participants: Alex (Product Owner), Sarah (Architect), Marcus (Backend Lead), Elena (Frontend Lead), and the User.
"""

        return full_prompt + conversation_note
