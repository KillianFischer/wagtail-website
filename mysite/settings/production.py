from .base import *

DEBUG = False

# DigitalOcean Spaces Configuration
AWS_ACCESS_KEY_ID = os.getenv('SPACES_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('SPACES_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('SPACES_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = f"https://{os.getenv('SPACES_REGION')}.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'media'
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

# Use DigitalOcean Spaces for media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Keep static files local (using whitenoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

try:
    from .local import *
except ImportError:
    pass