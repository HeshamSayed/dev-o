"""Service for communicating with external AI server - DEV-O Enhanced."""

import json
from typing import AsyncGenerator, Dict, Any, List
from django.conf import settings
import logging

from .external_ai_client import ExternalAIClient, ExternalAIConfig

logger = logging.getLogger(__name__)


class AIService:
    """Service for communicating with external AI server."""

    def __init__(self):
        # Initialize external AI client with config from settings
        config = ExternalAIConfig(
            base_url=settings.AI_SERVICE.get('BASE_URL', 'http://34.136.165.200:8000'),
            api_key=settings.AI_SERVICE.get('API_KEY', 'sk-test-123456'),
            model=settings.AI_SERVICE.get('DEFAULT_MODEL', 'deepseek-coder-optimized'),
            timeout=settings.AI_SERVICE.get('TIMEOUT', 120),
        )
        self.client = ExternalAIClient(config)


    def build_system_prompt(self, memories: List[Dict] = None) -> str:
        """Build system prompt with user memories."""
        base_prompt = """You are DEV-O, an AI-powered development assistant created to help build full-stack applications.
You are expert at Django, React, TypeScript, and modern web development.
You write clean, production-ready code with best practices and comprehensive documentation."""

        if memories:
            memory_text = "\n".join([f"- {m['key']}: {m['value']}" for m in memories])
            base_prompt += f"\n\nUser preferences and context:\n{memory_text}"

        return base_prompt

    def build_agent_system_prompt(
        self,
        agent_type: str,
        agent_prompt: str,
        project_context: Dict[str, Any]
    ) -> str:
        """Build system prompt for project agent."""
        file_tree = project_context.get('file_tree', {})

        prompt = f"""{agent_prompt}

CURRENT PROJECT STRUCTURE:
{json.dumps(file_tree, indent=2) if file_tree else '(Empty project - no files yet)'}

**IMPORTANT**: YOU MUST USE FILE TAGS FOR ALL CODE!

CRITICAL FILE FORMAT REQUIREMENTS:
You are working in PROJECT MODE. ALL code must be wrapped in <file> tags. NO code outside tags!

Format for creating/updating files:
<file path="path/to/file.py">
complete file content here
</file>

WORKFLOW - FOLLOW THIS EXACTLY (NO EXCEPTIONS):
1. Write ONE brief line: "Creating [filename]..."
2. Immediately write <file path="..."> tag
3. Put ALL code inside the tags
4. Close with </file>
5. Write ONE brief line: "✓ Created [filename]"
6. Move to next file if needed

ABSOLUTELY FORBIDDEN - NEVER DO THESE:
- ❌ NO markdown headings (###, ##, ####)
- ❌ NO "Step 1", "Step 2", "Let's...", "We'll..." tutorial format
- ❌ NO long explanations, tutorials, or educational content
- ❌ NO code in markdown blocks (```python, ```javascript, etc.)
- ❌ NO code examples outside <file> tags
- ❌ NO descriptions of what you're doing - JUST DO IT
- ⚠️ Users see code in the EDITOR not chat
- ⚠️ Chat is for brief status messages ONLY (1-2 words max)

Your thinking (optional):
<thinking>
your reasoning here
</thinking>

IMPORTANT RULES:
1. ALL code goes ONLY inside <file path="..."></file> tags
2. NO code, NO examples, NO snippets outside of file tags
3. Chat messages should be brief status updates only
4. Always write complete, working code - no placeholders
5. Include all necessary imports in each file
6. Follow best practices for {agent_type} development
7. Create files one at a time sequentially

EXAMPLE CORRECT RESPONSE:
"Creating models/user.py...

<file path="models/user.py">
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
</file>

✓ Created models/user.py"

WRONG RESPONSES - NEVER DO THESE:

❌ "### Step 1: Setting Up
Let's create the user model:
```python
class User...
```"

❌ "Here's the implementation. First we'll...
<file path='...'>...</file>
This handles authentication by..."

❌ "I'll create the model for managing users.
<file path='...'>...</file>
Next, we'll define the schema..."

✓ CORRECT: "Creating models/user.py...
<file>...</file>
✓ Created models/user.py"
"""
        logger.info(f"[AI_SERVICE] Built agent system prompt. Length: {len(prompt)} chars")
        logger.info(f"[AI_SERVICE] Prompt contains 'CRITICAL FILE FORMAT': {'CRITICAL FILE FORMAT' in prompt}")
        logger.info(f"[AI_SERVICE] Prompt contains '<file path=': {'<file path=' in prompt}")
        return prompt

    def prepare_messages(
        self,
        system_prompt: str,
        history: List[Any],
        user_message: str = None
    ) -> List[Dict[str, str]]:
        """Prepare messages array for AI API."""
        messages = [{"role": "system", "content": system_prompt}]

        for msg in history:
            messages.append({
                "role": msg.role if msg.role != 'agent' else 'assistant',
                "content": msg.content
            })

        if user_message:
            messages.append({"role": "user", "content": user_message})

        return messages

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        thinking_mode: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream chat completion from external AI server."""

        try:
            # Extract system and user messages
            system = next((m['content'] for m in messages if m['role'] == 'system'), None)

            # Build conversation history
            prompt_parts = []
            for msg in messages:
                if msg['role'] != 'system':
                    prompt_parts.append(f"{msg['role']}: {msg['content']}")

            prompt = "\n\n".join(prompt_parts)

            # Stream from external AI client
            async for chunk in self.client.generate_stream(
                prompt=prompt,
                system=system,
                temperature=temperature,
                max_tokens=max_tokens,
                thinking_mode=thinking_mode
            ):
                yield chunk  # Pass through all event types from client

            yield {'type': 'done'}

        except Exception as e:
            logger.error(f"AI service error: {e}")
            yield {'type': 'error', 'error': f'AI service error: {str(e)}'}
