"""Chat WebSocket consumer for normal chat mode."""

import json
import time
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import Conversation, Message
from apps.memory.models import UserMemory
from services.ai_service import AIService
from services.usage_service import UsageService

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for normal chat mode."""

    async def connect(self):
        """Handle WebSocket connection."""
        self.user = self.scope.get('user')

        if not self.user or not self.user.is_authenticated:
            await self.close(code=4001)
            return

        self.conversation_id = None
        await self.accept()

        # Send connected message
        await self.send(text_data=json.dumps({
            'type': 'connected',
            'message': 'Connected to chat'
        }))

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        pass

    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'ping':
                await self.send(text_data=json.dumps({'type': 'pong'}))
            else:
                await self.send_error(f'Unknown message type: {message_type}')

        except json.JSONDecodeError:
            await self.send_error('Invalid JSON')
        except Exception as e:
            await self.send_error(str(e))

    async def handle_chat_message(self, data):
        """Handle user chat message."""
        message_content = data.get('message')
        conversation_id = data.get('conversation_id')
        thinking_mode = data.get('thinking_mode', False)

        if not message_content:
            await self.send_error('Message content is required')
            return

        # Check usage limits
        can_send, used, limit = await self.check_chat_limit()
        if not can_send:
            await self.send_limit_error('chat', used, limit)
            return

        # Get or create conversation
        conversation = await self.get_or_create_conversation(conversation_id)

        # Update conversation title from first message
        await self.update_conversation_title(conversation, message_content)

        # Save user message
        await self.save_message(conversation, 'user', message_content)

        # Get user memories
        memories = await self.get_user_memories()

        # Stream AI response
        ai_service = AIService()
        system_prompt = ai_service.build_system_prompt(memories)
        history = await self.get_conversation_messages(conversation)
        messages = ai_service.prepare_messages(system_prompt, history, message_content)

        full_response = []
        full_thinking = []
        start_time = time.time()
        in_thinking = False

        try:
            async for chunk in ai_service.stream_chat(messages, thinking_mode=thinking_mode):
                if chunk['type'] == 'error':
                    await self.send_error(chunk['error'])
                    break

                elif chunk['type'] == 'thinking_start':
                    in_thinking = True
                    if thinking_mode:
                        await self.send(text_data=json.dumps({'type': 'thinking_start'}))

                elif chunk['type'] == 'thinking':
                    if thinking_mode:
                        full_thinking.append(chunk.get('content', ''))
                        await self.send(text_data=json.dumps({
                            'type': 'thinking',
                            'content': chunk.get('content', '')
                        }))

                elif chunk['type'] == 'thinking_end':
                    in_thinking = False
                    if thinking_mode:
                        await self.send(text_data=json.dumps({'type': 'thinking_end'}))

                elif chunk['type'] == 'done':
                    # Save assistant message with thinking if enabled
                    thinking_text = ''.join(full_thinking) if thinking_mode and full_thinking else None
                    await self.save_message_with_thinking(
                        conversation,
                        'assistant',
                        ''.join(full_response),
                        thinking_text
                    )

                    # Record usage
                    duration_ms = int((time.time() - start_time) * 1000)
                    await self.record_chat_usage(
                        conversation_id=str(conversation.id),
                        duration_ms=duration_ms
                    )

                    await self.send(text_data=json.dumps({
                        'type': 'done',
                        'conversation_id': str(conversation.id)
                    }))
                    break

                elif chunk['type'] == 'content':
                    full_response.append(chunk['content'])
                    await self.send(text_data=json.dumps({
                        'type': 'token',
                        'content': chunk['content']
                    }))

        except Exception as e:
            await self.send_error(str(e))

    async def send_error(self, error_message):
        """Send error message to client."""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'error': error_message
        }))

    # Database operations

    @database_sync_to_async
    def get_or_create_conversation(self, conversation_id=None):
        if conversation_id:
            try:
                return Conversation.objects.get(id=conversation_id, user=self.user)
            except Conversation.DoesNotExist:
                pass

        conversation = Conversation.objects.create(
            user=self.user,
            title='Chat'
        )
        return conversation

    @database_sync_to_async
    def get_conversation_messages(self, conversation):
        return list(conversation.messages.order_by('created_at')[:30])

    @database_sync_to_async
    def save_message(self, conversation, role, content):
        return Message.objects.create(
            conversation=conversation,
            role=role,
            content=content
        )

    @database_sync_to_async
    def save_message_with_thinking(self, conversation, role, content, thinking=None):
        return Message.objects.create(
            conversation=conversation,
            role=role,
            content=content,
            thinking=thinking
        )

    @database_sync_to_async
    def update_conversation_title(self, conversation, message_content):
        """Update conversation title based on first message if title is default."""
        # Check if this is a new conversation with default title
        if conversation.title in ['Chat', 'New Chat'] and conversation.messages.count() == 0:
            # Use first 50 characters of the message as title
            title = message_content[:50].strip()
            if len(message_content) > 50:
                title += '...'
            conversation.title = title
            conversation.save()

    @database_sync_to_async
    def get_user_memories(self):
        memories = UserMemory.objects.filter(user=self.user, is_active=True)
        return [{'key': m.key, 'value': m.value} for m in memories]

    # Usage tracking operations

    @database_sync_to_async
    def check_chat_limit(self):
        """Check if user can send chat message."""
        return UsageService.check_chat_limit(self.user)

    @database_sync_to_async
    def record_chat_usage(self, conversation_id, duration_ms=0):
        """Record chat message usage."""
        return UsageService.record_chat_message(
            user=self.user,
            conversation_id=conversation_id,
            duration_ms=duration_ms,
            model_used='default'
        )

    async def send_limit_error(self, limit_type, used, limit):
        """Send limit exceeded error with usage info."""
        usage_summary = await self.get_usage_summary()
        await self.send(text_data=json.dumps({
            'type': 'limit_exceeded',
            'limit_type': limit_type,
            'used': used,
            'limit': limit,
            'window_info': {
                'minutes_until_reset': usage_summary['window']['minutes_until_reset']
            },
            'message': f'You have reached your {limit_type} limit ({used}/{limit}). '
                      f'Resets in {usage_summary["window"]["minutes_until_reset"]} minutes. '
                      f'Upgrade to Pro for higher limits!'
        }))

    @database_sync_to_async
    def get_usage_summary(self):
        """Get current usage summary."""
        return UsageService.get_usage_summary(self.user)
