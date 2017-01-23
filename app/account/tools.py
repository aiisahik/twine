import models
import names
from django.contrib.auth.models import User
import random
from django.utils import timezone
from datetime import datetime

def generate_random_accounts(count=100, password='twine1234'):
    for index in range(count):
        gender = 'male' if index % 2 == 0 else 'female'
        ## ok this is hetero; will have to randomize this at some point
        gender_preference = 'male' if index % 2 == 1 else 'female'

        generated_name = names.get_full_name(gender=gender)
        generated_firstname = generated_name.split(' ')[0]
        generated_lastname = generated_name.split(' ')[1]
        generated_username = "%s.%d" % (generated_name.lower().replace(' ','.'), index)
        generated_email = "%s@gmail.com" % generated_username
        generated_user = User.objects.create_user(generated_username, generated_email, password)
        generated_user.first_name = generated_firstname
        generated_user.last_name = generated_lastname
        generated_user.save()
        generated_dob = datetime(timezone.now().year - random.randint(21,40), random.randint(1,12), random.randint(1,28), tzinfo=timezone.utc)

        generated_profile = models.Profile(user=generated_user,
                                first_name=generated_firstname,
                                last_name=generated_lastname,
                                gender=gender[0].upper(),
                                dob=generated_dob,
                                gender_preference=gender_preference[0].upper()
                            )
        generated_profile.save()
        print generated_profile, generated_user
