from django.conf import settings

def get_env_s3_key_prefix():
    """Gets the common Amazon S3 key prefix for current environment

    Should be grouped by environments that use the same DB servers
    """
    if settings.ENV_DEV or settings.ENV_QA:
        env = 'dev'
    elif settings.ENV_ALPHA:
        env = 'alpha'
    elif settings.ENV_PROD or settings.ENV_STAGE:
        env = 'prod'
    else:
        env = 'other'
    return env
