"""
Event Store

Handles event sourcing for the project.
All significant actions are logged as events for full traceability.
"""

import logging
from typing import Dict, Any, List, Optional
from django.db import transaction
from django.utils import timezone

from apps.context.models import EventLog
from apps.projects.models import Project

logger = logging.getLogger(__name__)


class EventStore:
    """
    Event store for event sourcing.

    Logs all significant events in the project for:
    1. Full audit trail
    2. Event replay capability
    3. Understanding project history
    4. Debugging and analysis
    """

    @staticmethod
    @transaction.atomic
    def log_event(
        project: Project,
        event_type: str,
        event_data: Dict[str, Any],
        actor_type: str = 'system',
        actor_id: str = ''
    ) -> EventLog:
        """
        Log a new event.

        Args:
            project: Project
            event_type: Type of event
            event_data: Event data (JSON)
            actor_type: Who triggered the event (agent, user, system)
            actor_id: ID of the actor

        Returns:
            Created EventLog instance
        """
        # Get next sequence number
        last_event = EventLog.objects.filter(
            project=project
        ).order_by('-sequence_number').first()

        sequence_number = (last_event.sequence_number + 1) if last_event else 1

        event = EventLog.objects.create(
            project=project,
            event_type=event_type,
            event_data=event_data,
            actor_type=actor_type,
            actor_id=actor_id,
            sequence_number=sequence_number
        )

        logger.debug(
            f"Event logged: [{sequence_number}] {event_type} by {actor_type}:{actor_id}"
        )

        return event

    @staticmethod
    def get_events(
        project: Project,
        event_type: Optional[str] = None,
        actor_type: Optional[str] = None,
        since_sequence: Optional[int] = None,
        limit: int = 100
    ) -> List[EventLog]:
        """
        Get events from the log.

        Args:
            project: Project
            event_type: Filter by event type
            actor_type: Filter by actor type
            since_sequence: Get events after this sequence number
            limit: Maximum number of events to return

        Returns:
            List of events
        """
        queryset = EventLog.objects.filter(project=project)

        if event_type:
            queryset = queryset.filter(event_type=event_type)

        if actor_type:
            queryset = queryset.filter(actor_type=actor_type)

        if since_sequence is not None:
            queryset = queryset.filter(sequence_number__gt=since_sequence)

        return list(queryset.order_by('sequence_number')[:limit])

    @staticmethod
    def get_project_timeline(
        project: Project,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get project timeline (recent events formatted for display).

        Args:
            project: Project
            limit: Number of events to return

        Returns:
            List of formatted event dicts
        """
        events = EventLog.objects.filter(
            project=project
        ).order_by('-sequence_number')[:limit]

        return [
            {
                "sequence": e.sequence_number,
                "type": e.event_type,
                "actor": f"{e.actor_type}:{e.actor_id}" if e.actor_id else e.actor_type,
                "timestamp": e.created_at.isoformat(),
                "data": e.event_data
            }
            for e in events
        ]

    @staticmethod
    def replay_events(
        project: Project,
        from_sequence: int = 0,
        to_sequence: Optional[int] = None
    ) -> List[EventLog]:
        """
        Replay events in order (for debugging or reconstruction).

        Args:
            project: Project
            from_sequence: Start sequence number
            to_sequence: End sequence number (None = all)

        Returns:
            List of events in sequence order
        """
        queryset = EventLog.objects.filter(
            project=project,
            sequence_number__gte=from_sequence
        )

        if to_sequence is not None:
            queryset = queryset.filter(sequence_number__lte=to_sequence)

        return list(queryset.order_by('sequence_number'))

    @staticmethod
    def get_event_statistics(project: Project) -> Dict[str, Any]:
        """
        Get statistics about events in the project.

        Args:
            project: Project

        Returns:
            Statistics dictionary
        """
        events = EventLog.objects.filter(project=project)

        stats = {
            "total_events": events.count(),
            "by_type": {},
            "by_actor": {}
        }

        for event in events:
            # Count by type
            event_type = event.event_type
            if event_type not in stats["by_type"]:
                stats["by_type"][event_type] = 0
            stats["by_type"][event_type] += 1

            # Count by actor
            actor = event.actor_type
            if actor not in stats["by_actor"]:
                stats["by_actor"][actor] = 0
            stats["by_actor"][actor] += 1

        return stats

    # Common event types for convenience

    @staticmethod
    def log_project_created(project: Project, user_id: str) -> EventLog:
        """Log project creation event."""
        return EventStore.log_event(
            project=project,
            event_type='project_created',
            event_data={
                "name": project.name,
                "description": project.description
            },
            actor_type='user',
            actor_id=user_id
        )

    @staticmethod
    def log_agent_hired(
        project: Project,
        agent_type: str,
        agent_id: str,
        hired_by: str
    ) -> EventLog:
        """Log agent hired event."""
        return EventStore.log_event(
            project=project,
            event_type='agent_hired',
            event_data={
                "agent_type": agent_type,
                "agent_id": agent_id,
                "hired_by": hired_by
            },
            actor_type='agent',
            actor_id=hired_by
        )

    @staticmethod
    def log_task_created(
        project: Project,
        task_id: str,
        task_title: str,
        created_by: str
    ) -> EventLog:
        """Log task creation event."""
        return EventStore.log_event(
            project=project,
            event_type='task_created',
            event_data={
                "task_id": task_id,
                "title": task_title
            },
            actor_type='agent',
            actor_id=created_by
        )

    @staticmethod
    def log_task_completed(
        project: Project,
        task_id: str,
        task_title: str,
        completed_by: str
    ) -> EventLog:
        """Log task completion event."""
        return EventStore.log_event(
            project=project,
            event_type='task_completed',
            event_data={
                "task_id": task_id,
                "title": task_title
            },
            actor_type='agent',
            actor_id=completed_by
        )

    @staticmethod
    def log_file_created(
        project: Project,
        file_path: str,
        created_by: str
    ) -> EventLog:
        """Log file creation event."""
        return EventStore.log_event(
            project=project,
            event_type='file_created',
            event_data={
                "file_path": file_path
            },
            actor_type='agent',
            actor_id=created_by
        )

    @staticmethod
    def log_decision_made(
        project: Project,
        decision_id: str,
        decision_title: str,
        made_by: str
    ) -> EventLog:
        """Log decision made event."""
        return EventStore.log_event(
            project=project,
            event_type='decision_made',
            event_data={
                "decision_id": decision_id,
                "title": decision_title
            },
            actor_type='agent',
            actor_id=made_by
        )
