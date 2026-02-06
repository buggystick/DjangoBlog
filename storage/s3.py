from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage
from django.conf import settings

class StaticStorage(S3Boto3Storage):
    bucket_name = getattr(settings, 'STATIC_BUCKET', 'blog-static')
    location = 'static'
    default_acl = 'public-read'
    querystring_auth = False
    file_overwrite = True

class ManifestStaticS3Storage(S3ManifestStaticStorage):
    bucket_name = getattr(settings, 'STATIC_BUCKET', 'blog-static')
    location = 'static'
    default_acl = 'public-read'
    querystring_auth = False
    file_overwrite = True

class MediaStorage(S3Boto3Storage):
    bucket_name = getattr(settings, 'MEDIA_BUCKET', 'blog-media')
    location = 'media'
    default_acl = 'private'
    querystring_auth = True
    file_overwrite = False
