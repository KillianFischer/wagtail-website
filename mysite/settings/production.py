from .base import *
from .storage import *

DEBUG = False

# Ensure SECRET_KEY is set in environment for production
if 'SECRET_KEY' not in os.environ:
    raise ImproperlyConfigured('SECRET_KEY environment variable is required in production')

try:
    from .local import *
except ImportError:
    pass