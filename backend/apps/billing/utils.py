"""
Utility functions for billing and referrals.
"""

import random
import string


def generate_referral_code(username: str) -> str:
    """
    Generate unique referral code from username.

    Args:
        username: User's username

    Returns:
        Unique referral code (e.g., DEV-O-ALEX1234)
    """
    from apps.billing.models_referral import ReferralCode

    # Create base from username (first 4 chars, uppercase)
    base = username.upper()[:4] if len(username) >= 4 else username.upper().ljust(4, 'X')

    # Remove special characters and spaces
    base = ''.join(c for c in base if c.isalnum())

    # Generate unique code
    max_attempts = 10
    for _ in range(max_attempts):
        # Add random 4-digit suffix
        suffix = ''.join(random.choices(string.digits, k=4))
        code = f"DEV-O-{base}{suffix}"

        # Check uniqueness
        if not ReferralCode.objects.filter(code=code).exists():
            return code

    # If still not unique, add more random chars
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"DEV-O-{suffix}"


def get_client_ip(request):
    """
    Get client IP address from request.

    Args:
        request: Django request object

    Returns:
        IP address string
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
