broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'US/Eastern'
enable_utc = True

#### celery settings 
#CELERY_RESULT_BACKEND = 'django-cache'
# CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = "redis"
imports = ("battle.tasks", )