from __future__ import absolute_import, unicode_literals
from .celery import app
from .models import Battle
from .tools import create_battles_for_judge
from account.models import Profile

from celery.schedules import crontab

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#     print "==========="
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)


@app.task
def test(arg):
    print(arg)

@app.task
def create_battles_for_judges(judges):
    for judge in judges: 
        create_battles_for_judge(judge)

@app.task
def create_battles_for_all():
    judges = Profile.objects.all()
    create_battles_for_judges(judges)
        
@app.task
def create_battles_for_judge_ids(judge_ids):
    print "judge_ids", judge_ids
    judges = Profile.objects.filter(user_id__in=judge_ids)
    print "judges", judges
    for judge in judges: 
        create_battles_for_judge(judge)
