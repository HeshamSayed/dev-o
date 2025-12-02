"""
Script to retroactively create files from existing agent messages that contain file tags.
"""

import os
import sys
import django

# Setup Django environment
sys.path.insert(0, '/opt/application/devo_code/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.chat.models import Message
from apps.projects.models import Project, ProjectFile
from services.agent_service import AgentService

# Get all agent messages
agent_messages = Message.objects.filter(role='agent').order_by('-created_at')

print(f"Found {agent_messages.count()} agent messages")

agent_service = AgentService()
total_files_created = 0

for msg in agent_messages:
    if '<file path=' not in msg.content:
        continue

    print(f"\n{'='*60}")
    print(f"Processing message {msg.id}")
    print(f"From conversation: {msg.conversation.id}")

    # Parse the message
    parsed = agent_service.parse_ai_response(msg.content)

    print(f"Found {len(parsed['files'])} files in message")

    if not parsed['files']:
        continue

    # Get the project from conversation
    project = msg.conversation.project
    if not project:
        print("No project associated with this conversation, skipping...")
        continue

    print(f"Project: {project.name} ({project.id})")

    # Create files
    for file_info in parsed['files']:
        print(f"  Creating file: {file_info['path']}")

        # Detect language from file extension
        ext_map = {
            '.py': 'python',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.md': 'markdown',
            '.sql': 'sql',
            '.sh': 'bash',
        }
        ext = '.' + file_info['path'].split('.')[-1].lower() if '.' in file_info['path'] else ''
        language = ext_map.get(ext, 'text')

        # Create or update file
        file_obj, created = ProjectFile.objects.update_or_create(
            project=project,
            path=file_info['path'],
            defaults={
                'content': file_info['content'],
                'language': language,
                'created_by_agent': msg.agent,
            }
        )

        if created:
            print(f"    ✓ Created: {file_info['path']} ({language})")
            total_files_created += 1
        else:
            file_obj.version += 1
            file_obj.save()
            print(f"    ✓ Updated: {file_info['path']} (version {file_obj.version})")
            total_files_created += 1

    # Update the message content to remove file tags
    msg.content = parsed['chat_content']
    msg.save()
    print(f"  Updated message content (removed file tags)")

print(f"\n{'='*60}")
print(f"DONE! Created/updated {total_files_created} files")
print(f"{'='*60}")
