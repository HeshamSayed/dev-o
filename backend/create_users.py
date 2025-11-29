#!/usr/bin/env python
"""Script to create superuser and hesham user with enterprise tier"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devo.settings')
django.setup()

from apps.accounts.models import User, Subscription
from datetime import datetime, timedelta

def create_users():
    """Create superuser and hesham user with enterprise tier"""

    # Create superuser if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@devtools-co.com',
            password='admin123'
        )
        print(f"✅ Superuser 'admin' created successfully")
        print(f"   Username: admin")
        print(f"   Password: admin123")
    else:
        print("ℹ️  Superuser 'admin' already exists")

    # Create hesham user with enterprise tier
    if not User.objects.filter(username='hesham').exists():
        hesham = User.objects.create_user(
            username='hesham',
            email='hesham@devtools-co.com',
            password='hesham123',
            is_staff=True  # Give staff access
        )

        # Create enterprise subscription with unlimited limits
        subscription = Subscription.objects.create(
            user=hesham,
            tier='enterprise',
            is_active=True,
            max_projects=-1,  # unlimited
            max_agents_per_project=-1,  # unlimited
            max_actions_per_day=-1,  # unlimited
            can_use_api_llms=True,
            can_use_custom_agents=True,
            expires_at=datetime.now() + timedelta(days=365)  # 1 year
        )

        print(f"✅ User 'hesham' created successfully with ENTERPRISE tier")
        print(f"   Username: hesham")
        print(f"   Password: hesham123")
        print(f"   Tier: {subscription.tier}")
        print(f"   Active: {subscription.is_active}")
        print(f"   Max Projects: Unlimited")
        print(f"   Max Agents: Unlimited")
        print(f"   Max Actions/Day: Unlimited")
        print(f"   Valid until: {subscription.expires_at.strftime('%Y-%m-%d')}")
    else:
        hesham = User.objects.get(username='hesham')
        # Update subscription to enterprise if it exists
        subscription, created = Subscription.objects.get_or_create(
            user=hesham,
            defaults={
                'tier': 'enterprise',
                'is_active': True,
                'max_projects': -1,
                'max_agents_per_project': -1,
                'max_actions_per_day': -1,
                'can_use_api_llms': True,
                'can_use_custom_agents': True,
                'expires_at': datetime.now() + timedelta(days=365)
            }
        )
        if not created:
            subscription.tier = 'enterprise'
            subscription.is_active = True
            subscription.max_projects = -1
            subscription.max_agents_per_project = -1
            subscription.max_actions_per_day = -1
            subscription.can_use_api_llms = True
            subscription.can_use_custom_agents = True
            subscription.save()
        print(f"ℹ️  User 'hesham' already exists - updated to ENTERPRISE tier")

    print("\n" + "="*60)
    print("USER ACCOUNTS READY")
    print("="*60)

if __name__ == '__main__':
    create_users()
