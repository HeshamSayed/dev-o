"""
Management command to seed DEV-O pricing plans.

Usage:
    python manage.py seed_plans
"""

from django.core.management.base import BaseCommand
from apps.billing.models import Plan


class Command(BaseCommand):
    help = 'Seeds the database with DEV-O pricing plans (2-hour reset windows)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding DEV-O pricing plans...'))

        plans_data = [
            {
                'name': 'Free',
                'plan_type': 'free',
                'price_monthly': 0,
                'price_yearly': 0,
                # Chat limits (per 2-hour window)
                'messages_per_window': 10,
                'max_conversations': 5,
                'context_window': 4096,
                # Project limits (per 2-hour window)
                'max_active_projects': 1,
                'max_archived_projects': 0,
                'max_files_per_project': 10,
                'project_requests_per_window': 2,
                # Agent limits
                'available_agents': ['Marcus - Backend Lead'],
                'max_concurrent_agents': 1,
                # Storage limits
                'storage_limit_mb': 10,
                'max_file_size_kb': 100,
                'retention_days': 7,
                # AI Model
                'model_tier': 'basic',
                'max_output_tokens': 1024,
                # Rate limits
                'requests_per_minute': 2,
                'max_concurrent_connections': 1,
                'queue_priority': 0,
                # Features
                'has_thinking_mode': False,
                'has_download': False,
                'has_git_integration': False,
                'has_api_access': False,
                'has_chat_search': False,
            },
            {
                'name': 'Pro',
                'plan_type': 'pro',
                'price_monthly': 19,
                'price_yearly': 190,  # ~17% discount
                # Chat limits (per 2-hour window)
                'messages_per_window': 100,
                'max_conversations': 50,
                'context_window': 16384,
                # Project limits (per 2-hour window)
                'max_active_projects': 5,
                'max_archived_projects': 20,
                'max_files_per_project': 100,
                'project_requests_per_window': 20,
                # Agent limits
                'available_agents': [
                    'Marcus - Backend Lead',
                    'Elena - Frontend Lead',
                    'DevOps Engineer',
                    'Sarah - Solution Architect'
                ],
                'max_concurrent_agents': 2,
                # Storage limits
                'storage_limit_mb': 1000,  # 1GB
                'max_file_size_kb': 5120,  # 5MB
                'retention_days': 90,
                # AI Model
                'model_tier': 'advanced',
                'max_output_tokens': 4096,
                # Rate limits
                'requests_per_minute': 20,
                'max_concurrent_connections': 5,
                'queue_priority': 10,
                # Features
                'has_thinking_mode': True,
                'has_download': True,
                'has_git_integration': True,
                'has_api_access': False,
                'has_chat_search': True,
            },
            {
                'name': 'Team',
                'plan_type': 'team',
                'price_monthly': 49,
                'price_yearly': 490,  # ~17% discount
                # Chat limits (per 2-hour window)
                'messages_per_window': 500,
                'max_conversations': -1,  # Unlimited
                'context_window': 32768,
                # Project limits (per 2-hour window)
                'max_active_projects': 20,
                'max_archived_projects': -1,  # Unlimited
                'max_files_per_project': 500,
                'project_requests_per_window': 100,
                # Agent limits
                'available_agents': [
                    'Marcus - Backend Lead',
                    'Elena - Frontend Lead',
                    'DevOps Engineer',
                    'Sarah - Solution Architect'
                ],
                'max_concurrent_agents': 4,
                # Storage limits
                'storage_limit_mb': 10240,  # 10GB
                'max_file_size_kb': 10240,  # 10MB
                'retention_days': 365,
                # AI Model
                'model_tier': 'premium',
                'max_output_tokens': 8192,
                # Rate limits
                'requests_per_minute': 100,
                'max_concurrent_connections': 20,
                'queue_priority': 50,
                # Features
                'has_thinking_mode': True,
                'has_download': True,
                'has_git_integration': True,
                'has_api_access': True,
                'has_chat_search': True,
            },
            {
                'name': 'Enterprise',
                'plan_type': 'enterprise',
                'price_monthly': 0,  # Custom pricing
                'price_yearly': 0,    # Custom pricing
                # Chat limits (per 2-hour window)
                'messages_per_window': -1,  # Unlimited
                'max_conversations': -1,     # Unlimited
                'context_window': 65536,
                # Project limits (per 2-hour window)
                'max_active_projects': -1,   # Unlimited
                'max_archived_projects': -1,  # Unlimited
                'max_files_per_project': -1,  # Unlimited
                'project_requests_per_window': -1,  # Unlimited
                # Agent limits
                'available_agents': [
                    'Marcus - Backend Lead',
                    'Elena - Frontend Lead',
                    'DevOps Engineer',
                    'Sarah - Solution Architect'
                ],
                'max_concurrent_agents': -1,  # Unlimited
                # Storage limits
                'storage_limit_mb': -1,   # Unlimited
                'max_file_size_kb': -1,   # Unlimited
                'retention_days': -1,      # Unlimited
                # AI Model
                'model_tier': 'enterprise',
                'max_output_tokens': 16384,
                # Rate limits
                'requests_per_minute': -1,  # Unlimited
                'max_concurrent_connections': -1,  # Unlimited
                'queue_priority': 100,
                # Features
                'has_thinking_mode': True,
                'has_download': True,
                'has_git_integration': True,
                'has_api_access': True,
                'has_chat_search': True,
            },
        ]

        created_count = 0
        updated_count = 0

        for plan_data in plans_data:
            plan, created = Plan.objects.update_or_create(
                plan_type=plan_data['plan_type'],
                defaults=plan_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created plan: {plan.name} (${plan.price_monthly}/mo)')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Updated plan: {plan.name} (${plan.price_monthly}/mo)')
                )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Created {created_count}, Updated {updated_count} plans.'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                'Note: All limits are per 2-hour window! Resets every 2 hours for better engagement.'
            )
        )
