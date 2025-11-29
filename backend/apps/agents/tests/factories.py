"""
Factories for agents app models.
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.agents.models import AgentType, AgentInstance, AgentMessage, AgentAction
from apps.projects.tests.factories import ProjectFactory

fake = Faker()


class AgentTypeFactory(DjangoModelFactory):
    """Factory for AgentType model."""

    class Meta:
        model = AgentType
        django_get_or_create = ('role',)

    name = factory.Sequence(lambda n: f'Agent Type {n}')
    role = factory.Sequence(lambda n: f'role_{n}')
    description = factory.Faker('paragraph')
    system_prompt = factory.Faker('text')
    available_tools = ['read_file', 'write_file', 'create_task']
    can_hire = []
    hierarchy_level = 1
    default_model = 'deepseek-r1:7b'
    default_temperature = 0.7
    max_iterations = 10
    is_active = True


class AgentInstanceFactory(DjangoModelFactory):
    """Factory for AgentInstance model."""

    class Meta:
        model = AgentInstance

    project = factory.SubFactory(ProjectFactory)
    agent_type = factory.SubFactory(AgentTypeFactory)
    status = 'idle'
    status_message = 'Ready'
    working_memory = factory.Dict({})
    conversation_history = factory.List([])
    tasks_completed = 0
    errors_encountered = 0
    total_tokens_used = 0


class AgentMessageFactory(DjangoModelFactory):
    """Factory for AgentMessage model."""

    class Meta:
        model = AgentMessage

    project = factory.SubFactory(ProjectFactory)
    from_agent = factory.SubFactory(AgentInstanceFactory)
    message_type = 'task_assignment'
    content = factory.Dict({'message': factory.Faker('sentence')})
    requires_response = False
    responded = False


class AgentActionFactory(DjangoModelFactory):
    """Factory for AgentAction model."""

    class Meta:
        model = AgentAction

    project = factory.SubFactory(ProjectFactory)
    agent = factory.SubFactory(AgentInstanceFactory)
    action_type = 'file_created'
    action_data = factory.Dict({'file_path': 'test.py'})
    is_reversible = True
    status = 'completed'
