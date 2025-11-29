"""
Django settings module.

Import from .development or .production based on environment.
"""

from decouple import config

ENV = config('DJANGO_ENV', default='development')

if ENV == 'production':
    from .production import *
else:
    from .development import *
