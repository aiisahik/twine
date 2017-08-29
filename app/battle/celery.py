from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'twine.settings')

app = Celery(
    'tasks', 
)
app.config_from_object('twine.celeryconfig')
app.conf.beat_schedule = {
    'create-all-battles-every-hour': {
        'task': 'battle.tasks.create_battles_for_all',
        'schedule': 3600.0,
        'args': ()
    },
}

if __name__ == '__main__':
    app.start()