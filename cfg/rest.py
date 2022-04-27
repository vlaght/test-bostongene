DATABASE_URLS = {
    'main': "postgresql://root@localhost:5432/db",
    'test': "postgresql://root@localhost:5432/db_test",
}

MEDIA_PATH = 'media/'


CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
