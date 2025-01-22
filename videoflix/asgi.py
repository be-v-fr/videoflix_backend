"""
ASGI config for videoflix project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoflix.settings')
os.environ.setdefault('FRONTEND_BASE_URL', 'https://videoflix.bengt-fruechtenicht.de/')

application = get_asgi_application()
