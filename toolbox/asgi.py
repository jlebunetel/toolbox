"""ASGI config for toolbox project."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolbox.settings")
application = get_asgi_application()
