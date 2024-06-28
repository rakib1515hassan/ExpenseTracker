from config.env import env


# STORAGES setting: Starting with Django 4.2, default file storage engine
# can be configured with the STORAGES setting under the default key, but before use DEFAULT_FILE_STORAGE.

# Previously: 
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Present:
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {},
    },
}




AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY   = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME   = env("AWS_S3_REGION_NAME")
AWS_S3_ENDPOINT_URL  = env("AWS_S3_ENDPOINT_URL")
AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")

AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_FILE_OVERWRITE    = True


# AWS_ACCESS_KEY_ID = 'your-access-key-id'
# AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'
# AWS_STORAGE_BUCKET_NAME = 'your-s3-bucket-name'
# AWS_S3_REGION_NAME = 'your-region'  # e.g., us-east-1
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# # For serving static files directly from S3
# AWS_S3_URL_PROTOCOL = 'https'
# AWS_S3_USE_SSL = True
# AWS_S3_VERIFY = True

# # Static and media file configuration
# STATIC_URL = f'{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/static/'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# MEDIA_URL = f'{AWS_S3_URL_PROTOCOL}://{AWS_S3_CUSTOM_DOMAIN}/media/'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'pt