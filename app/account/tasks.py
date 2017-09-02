from __future__ import absolute_import, unicode_literals
from .celery import app
from .models import Profile, PreferenceMatch
from celery.schedules import crontab

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
#     print "==========="
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)


@app.task
def create_preference_matches(user_ids):
    new_preference_matches = []
    profiles = Profile.objects.filter(user_id__in=user_ids)
    for profile in profiles: 
        print "creating preference match for ", profiles
        matched_profiles = Profile.objects.get_matches(profile)
        for match in matched_profiles:
            new_preference_matches.append(
                PreferenceMatch(
                    profile=profile,
                    target=match,
                )
            )
    created_preference_matches = PreferenceMatch.objects.bulk_create(new_preference_matches)
    print "created %d preference matches for %d profiles" % (len(created_preference_matches), len(user_ids))
    
