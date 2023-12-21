import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

# Trying to import Django Configuration’s get_asgi_application 
# will fail if DJANGO_CONFIGURATION is not yet defined
from configurations.asgi import get_asgi_application

application = get_asgi_application()
