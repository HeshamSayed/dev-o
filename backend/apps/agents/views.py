"""
Agent APIViews

Agent management and execution endpoints.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import StreamingHttpResponse
from django.db import models

from .models import AgentInstance, AgentType, AgentMessage, AgentAction
from .serializers import (
    AgentInstanceSerializer,
    AgentInstanceListSerializer,
    AgentHireSerializer,
    AgentTypeSerializer,
    AgentTypeListSerializer,
    AgentMessageSerializer,
    AgentMessageCreateSerializer,
    AgentActionSerializer,
    AgentActionListSerializer,
    AgentStatusSerializer
)
from apps.projects.models import Project
from apps.tasks.models import Task


class AgentTypeListView(APIView):
    """
    Agent types list endpoint.

    GET /api/agent-types/ - List all available agent types
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List available agent types."""
        agent_types = AgentType.objects.filter(is_active=True)
        serializer = AgentTypeListSerializer(agent_types, many=True)
        return Response(serializer.data)


class AgentTypeDetailView(APIView):
    """
    Agent type detail endpoint.

    GET /api/agent-types/{id}/ - Get agent type details
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get agent type details."""
        try:
            agent_type = AgentType.objects.get(id=pk, is_active=True)
        except AgentType.DoesNotExist:
            return Response({
                'error': 'Agent type not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AgentTypeSerializer(agent_type)
        return Response(serializer.data)


class AgentListView(APIView):
    """
    Project agents list endpoint.

    GET /api/projects/{project_id}/agents/ - List project agents
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """List project's agents."""
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        agents = AgentInstance.objects.filter(
            project=project
        ).select_related('agent_type', 'current_task').order_by('-created_at')

        serializer = AgentInstanceListSerializer(agents, many=True)
        return Response(serializer.data)


class AgentHireView(APIView):
    """
    Hire agent endpoint.

    POST /api/projects/{project_id}/agents/ - Hire new agent
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        """Hire new agent."""
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AgentHireSerializer(
            data=request.data,
            context={'project': project, 'hiring_agent': None}
        )

        if serializer.is_valid():
            agent = serializer.save()
            return Response(
                AgentInstanceSerializer(agent).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentDetailView(APIView):
    """
    Agent detail endpoint.

    GET /api/agents/{id}/ - Get agent details
    PATCH /api/agents/{id}/ - Update agent
    DELETE /api/agents/{id}/ - Remove agent
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        """Get agent if user has access."""
        try:
            return AgentInstance.objects.select_related(
                'agent_type', 'project', 'current_task'
            ).get(
                id=pk,
                project__owner=request.user
            )
        except AgentInstance.DoesNotExist:
            return None

    def get(self, request, pk):
        """Get agent details."""
        agent = self.get_object(request, pk)

        if not agent:
            return Response({
                'error': 'Agent not found'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AgentInstanceSerializer(agent)
        return Response(serializer.data)

    def patch(self, request, pk):
        """Update agent."""
        agent = self.get_object(request, pk)

        if not agent:
            return Response({
                'error': 'Agent not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Only allow updating status and status_message
        allowed_fields = ['status', 'status_message', 'model', 'temperature']
        data = {k: v for k, v in request.data.items() if k in allowed_fields}

        serializer = AgentInstanceSerializer(agent, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Remove agent."""
        agent = self.get_object(request, pk)

        if not agent:
            return Response({
                'error': 'Agent not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if agent can be deleted
        if agent.status == 'working':
            return Response({
                'error': 'Cannot delete agent that is currently working'
            }, status=status.HTTP_400_BAD_REQUEST)

        agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AgentMessagesView(APIView):
    """
    Agent messages endpoint.

    GET /api/agents/{id}/messages/ - Get agent messages
    POST /api/agents/{id}/messages/ - Send message to agent
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get agent messages."""
        try:
            agent = AgentInstance.objects.get(
                id=pk,
                project__owner=request.user
            )
        except AgentInstance.DoesNotExist:
            return Response({
                'error': 'Agent not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Get messages to and from this agent
        messages = AgentMessage.objects.filter(
            project=agent.project
        ).filter(
            models.Q(from_agent=agent) | models.Q(to_agent=agent)
        ).select_related('from_agent', 'to_agent').order_by('-created_at')[:50]

        serializer = AgentMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        """Send message to agent."""
        try:
            to_agent = AgentInstance.objects.get(
                id=pk,
                project__owner=request.user
            )
        except AgentInstance.DoesNotExist:
            return Response({
                'error': 'Agent not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Get user's orchestrator agent as sender (simplified)
        from_agent = AgentInstance.objects.filter(
            project=to_agent.project,
            agent_type__role='orchestrator'
        ).first()

        if not from_agent:
            return Response({
                'error': 'No orchestrator agent found'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = AgentMessageCreateSerializer(
            data=request.data,
            context={
                'project': to_agent.project,
                'from_agent': from_agent
            }
        )

        if serializer.is_valid():
            message = serializer.save()
            return Response(
                AgentMessageSerializer(message).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentActionsView(APIView):
    """
    Agent actions endpoint.

    GET /api/agents/{id}/actions/ - Get agent actions history
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Get agent actions."""
        try:
            agent = AgentInstance.objects.get(
                id=pk,
                project__owner=request.user
            )
        except AgentInstance.DoesNotExist:
            return Response({
                'error': 'Agent not found'
            }, status=status.HTTP_404_NOT_FOUND)

        actions = AgentAction.objects.filter(
            agent=agent
        ).select_related('task').order_by('-created_at')[:100]

        serializer = AgentActionListSerializer(actions, many=True)
        return Response(serializer.data)


class AgentExecuteView(APIView):
    """
    Agent execution endpoint.

    POST /api/agents/{id}/execute/ - Execute agent with a task
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        """Execute agent with task."""
        try:
            agent = AgentInstance.objects.get(
                id=pk,
                project__owner=request.user
            )
        except AgentInstance.DoesNotExist:
            return Response({
                'error': 'Agent not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Get task
        task_id = request.data.get('task_id')
        if not task_id:
            return Response({
                'error': 'task_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(
                id=task_id,
                project=agent.project
            )
        except Task.DoesNotExist:
            return Response({
                'error': 'Task not found'
            }, status=status.HTTP_404_NOT_FOUND)

        # Check if agent is already working
        if agent.status == 'working':
            return Response({
                'error': 'Agent is already working on a task'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Execute agent asynchronously
        from apps.agents.engine.executor import AgentExecutor
        import asyncio

        async def execute():
            async for event in AgentExecutor.execute_agent(agent, task, stream=True):
                yield event

        # For now, return success response
        # In production, this would use WebSockets or Server-Sent Events
        return Response({
            'message': 'Agent execution started',
            'agent_id': str(agent.id),
            'task_id': str(task.id)
        }, status=status.HTTP_202_ACCEPTED)


class ProjectExecuteView(APIView):
    """
    Project execution endpoint.

    POST /api/projects/{project_id}/execute/ - Execute project with user message
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        """Execute project with user message."""
        try:
            project = Project.objects.get(id=project_id, owner=request.user)
        except Project.DoesNotExist:
            return Response({
                'error': 'Project not found'
            }, status=status.HTTP_404_NOT_FOUND)

        message = request.data.get('message')
        if not message:
            return Response({
                'error': 'message is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if streaming is requested
        stream = request.data.get('stream', False)

        if stream:
            # Return streaming response
            from apps.agents.engine.executor import AgentExecutor
            import asyncio
            import json

            def event_stream():
                async def execute():
                    async for event in AgentExecutor.execute_project(project, message, stream=True):
                        yield f"data: {json.dumps(event)}\n\n"

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    async_gen = execute()
                    while True:
                        try:
                            event = loop.run_until_complete(async_gen.__anext__())
                            yield event
                        except StopAsyncIteration:
                            break
                finally:
                    loop.close()

            response = StreamingHttpResponse(
                event_stream(),
                content_type='text/event-stream'
            )
            response['Cache-Control'] = 'no-cache'
            response['X-Accel-Buffering'] = 'no'
            return response
        else:
            # Execute asynchronously and return task ID
            from apps.agents.engine.executor import AgentExecutor
            import asyncio

            # Create a task for tracking
            task = Task.objects.create(
                project=project,
                title=f"Execute: {message[:50]}",
                description=message,
                status='pending'
            )

            # Execute in background
            async def execute_async():
                result_text = ""
                async for event in AgentExecutor.execute_project(project, message, stream=True):
                    if event.get('type') == 'message':
                        result_text += event.get('content', '') + "\n"
                    elif event.get('type') == 'code':
                        result_text += f"```{event.get('language', '')}\n{event.get('content', '')}\n```\n"

                task.status = 'completed'
                task.result = result_text
                task.save()

            # Run in background
            import threading
            def run_async():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(execute_async())
                loop.close()

            thread = threading.Thread(target=run_async)
            thread.start()

            return Response({
                'message': 'Project execution started',
                'project_id': str(project.id),
                'task_id': str(task.id)
            }, status=status.HTTP_202_ACCEPTED)
