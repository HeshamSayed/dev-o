"""
Factories for tasks app models.
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.tasks.models import Task, TaskDependency, TaskLog
from apps.projects.tests.factories import ProjectFactory
from apps.agents.tests.factories import AgentInstanceFactory

fake = Faker()


class TaskFactory(DjangoModelFactory):
    """Factory for Task model."""

    class Meta:
        model = Task

    project = factory.SubFactory(ProjectFactory)
    title = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    task_type = 'task'
    status = 'todo'
    priority = 3
    requirements = factory.Dict({})
    acceptance_criteria = factory.Dict({})
    deliverables = factory.List([])
    estimated_effort = 0
    actual_effort = 0
    iteration_count = 0


class TaskDependencyFactory(DjangoModelFactory):
    """Factory for TaskDependency model."""

    class Meta:
        model = TaskDependency

    task = factory.SubFactory(TaskFactory)
    depends_on = factory.SubFactory(TaskFactory)
    dependency_type = 'blocking'


class TaskLogFactory(DjangoModelFactory):
    """Factory for TaskLog model."""

    class Meta:
        model = TaskLog

    task = factory.SubFactory(TaskFactory)
    agent = factory.SubFactory(AgentInstanceFactory)
    log_type = 'comment'
    content = factory.Faker('paragraph')
    metadata = factory.Dict({})
