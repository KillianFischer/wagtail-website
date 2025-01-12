from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class CustomS3Storage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'original_images'
    file_overwrite = False
    default_acl = 'public-read'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    url_protocol = 'https:'
    endpoint_url = settings.AWS_S3_ENDPOINT_URL

class RenditionS3Storage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = 'images'
    file_overwrite = False
    default_acl = 'public-read'
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    url_protocol = 'https:'
    endpoint_url = settings.AWS_S3_ENDPOINT_URL