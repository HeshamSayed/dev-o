"""
Factories for projects app models.
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker

from apps.projects.models import Project, ProjectCheckpoint
from apps.accounts.tests.factories import UserFactory

fake = Faker()


class ProjectFactory(DjangoModelFactory):
    """Factory for Project model."""

    class Meta:
        model = Project

    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f'Project {n}')
    description = factory.Faker('paragraph')
    status = 'initializing'
    manifest = factory.Dict({
        'requirements': {},
        'tech_stack': {},
        'architecture': {}
    })
    settings = factory.Dict({})


class ProjectCheckpointFactory(DjangoModelFactory):
    """Factory for ProjectCheckpoint model."""

    class Meta:
        model = ProjectCheckpoint

    project = factory.SubFactory(ProjectFactory)
    name = factory.Sequence(lambda n: f'Checkpoint {n}')
    description = factory.Faker('sentence')
    state_snapshot = factory.Dict({})
    created_by = 'user'
    is_auto = False
