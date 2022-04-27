DATABASE_URLS = {
    'main': "postgresql://root@db/db",
    'test': "postgresql://root@db/db_test",
}

MEDIA_PATH = '/media/'
CELERY_BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
