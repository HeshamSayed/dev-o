"""Project serializers."""

from rest_framework import serializers
from .models import Project, ProjectFile
from apps.agents.models import Agent, AgentAssignment


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'path', 'content', 'language', 'version', 'created_at', 'updated_at']
        read_only_fields = ['id', 'version', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    file_count = serializers.SerializerMethodField()
    agents = serializers.SerializerMethodField()
    file_tree = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'project_type', 'status',
            'file_count', 'agents', 'file_tree', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def get_file_count(self, obj):
        return obj.files.count()

    def get_agents(self, obj):
        assignments = obj.agent_assignments.filter(is_active=True)
        return [
            {'id': str(a.agent.id), 'name': a.agent.name, 'type': a.agent.type}
            for a in assignments
        ]

    def get_file_tree(self, obj):
        return obj.get_file_tree()


class CreateProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    project_type = serializers.ChoiceField(choices=Project.PROJECT_TYPES)
    agent_types = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=['backend', 'frontend', 'devops']
    )

    def create(self, validated_data):
        user = self.context['request'].user
        agent_types = validated_data.pop('agent_types', ['backend', 'frontend', 'devops'])

        # Create project
        project = Project.objects.create(
            user=user,
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            project_type=validated_data['project_type']
        )

        # Assign agents
        for agent_type in agent_types:
            agent = Agent.objects.filter(type=agent_type, is_active=True).first()
            if agent:
                AgentAssignment.objects.create(project=project, agent=agent)

        return project
