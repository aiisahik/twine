import models
import names
from django.contrib.auth.models import User
import random
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime
from battle.tasks import create_battles_for_judge_ids

MIN_MALE_HEIGHT = 160
MAX_MALE_HEIGHT = 240

MIN_FEMALE_HEIGHT = 145
MAX_FEMALE_HEIGHT = 190

HEIGHT_BIAS = 10

AGE_FLEXIBILITY = 3

def generate_random_accounts(count=100, password='twine1234'):
    new_users = []
    new_profiles = []
    username_gender_dict = {}
    for index in range(count):
        
        gender = 'male' if index % 2 == 0 else 'female'
        ## ok this is hetero; will have to randomize this at some point
        generated_name = names.get_full_name(gender=gender)
        generated_firstname = generated_name.split(' ')[0]
        generated_lastname = generated_name.split(' ')[1]

        # generate a new user
        generated_username = "%s.%d" % (generated_name.lower().replace(' ','.'), index)
        generated_email = "%s@gmail.com" % generated_username
        generated_user = User(
            username=generated_username, 
            email=generated_email, 
            password=password, 
            first_name=generated_firstname,
            last_name=generated_lastname,
            is_active=True
        )
        new_users.append(generated_user)
        username_gender_dict[generated_username] = gender
    created_users = User.objects.bulk_create(new_users)
    for created_user in created_users:
        ## gender 
        gender = username_gender_dict.get(created_user.username)
        sexuality_dice = random.randint(0,100)
        ## age 
        age_years = random.randint(21,40)
        generated_dob = datetime(timezone.now().year - age_years, random.randint(1,12), random.randint(1,28), tzinfo=timezone.utc)
        ## the men 
        if gender == 'male':
            if sexuality_dice < 5:
                gender_preference = 'M'
            elif sexuality_dice < 8:
                gender_preference = 'MF'
            else: 
                gender_preference = 'F'
            min_age_preference = random.randint(int(age_years/2+7 - AGE_FLEXIBILITY),int(age_years/2+7 + AGE_FLEXIBILITY))
            max_age_preference = random.randint(int(age_years - AGE_FLEXIBILITY/2),int(age_years + AGE_FLEXIBILITY))
            generated_height = random.randint(MIN_MALE_HEIGHT,MAX_MALE_HEIGHT)
            min_height_preference = random.randint(MIN_FEMALE_HEIGHT,MIN_FEMALE_HEIGHT + HEIGHT_BIAS * 2)
            max_height_preference = random.randint(min_height_preference,max(min_height_preference, generated_height + HEIGHT_BIAS))
        else: 
        ## the women 
            if sexuality_dice < 2:
                gender_preference = 'F'
            elif sexuality_dice < 6:
                gender_preference = 'MF'
            else: 
                gender_preference = 'M'
            min_age_preference = random.randint(age_years - AGE_FLEXIBILITY,age_years + AGE_FLEXIBILITY)
            max_age_preference = random.randint(int(age_years * 1.4 - AGE_FLEXIBILITY),int(age_years * 1.4 + AGE_FLEXIBILITY * 2))
            generated_height = random.randint(MIN_FEMALE_HEIGHT,MAX_FEMALE_HEIGHT)
            min_height_preference = random.randint(min(generated_height + HEIGHT_BIAS, MAX_MALE_HEIGHT),MAX_MALE_HEIGHT)
            max_height_preference = random.randint(min(min_height_preference + HEIGHT_BIAS, MAX_MALE_HEIGHT),MAX_MALE_HEIGHT)

        generated_profile = models.Profile(user=created_user,
                                first_name=created_user.first_name,
                                last_name=created_user.last_name,
                                gender=gender[0].upper(),
                                dob=generated_dob,
                                min_age_preference=min_age_preference,
                                max_age_preference=max_age_preference,
                                gender_preference=gender_preference,
                                height=generated_height,
                                min_height_preference=min_height_preference,
                                max_height_preference=max_height_preference
                            )
        new_profiles.append(generated_profile)
        print generated_profile, created_user
    created_profiles = models.Profile.objects.bulk_create(new_profiles)
    ## traits 
    new_trait_identities = []
    new_trait_preferences = []
    
    for created_profile in created_profiles:
        ## race identity and preferences 
        num_races = models.Trait.objects.filter(type__name='race').count()
        num_racial_preferences = random.randint(1,num_races)
        random_race_ids = random.sample(range(num_races), num_racial_preferences)
        random_races = models.Trait.objects.filter(id__in=random_race_ids)
        new_trait_identities.append(
            models.TraitIdentity(
                profile=created_profile,
                strength=random.randint(1,10),
                trait=random_races.first() # first random trait is profile identity 
            )
        )

        for index, random_race in enumerate(random_races):
            race_preference_level = random.randint(5,10) if index==1 else random.randint(1,10)
            new_trait_preferences.append(
                models.TraitPreference(
                    profile=created_profile,
                    strength=race_preference_level,
                    trait=random_race
                )
            )
    created_trait_identities = models.TraitIdentity.objects.bulk_create(new_trait_identities)
    created_trait_preferences = models.TraitPreference.objects.bulk_create(new_trait_preferences)

    created_profile_ids = [profile.user_id for profile in created_profiles]
    create_battles_for_judge_ids.apply_async((created_profile_ids,), retry=True, retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.2,
    })


def populate_race_ethnicity():
    race_ethnicity_map = { 
        "asian" : [
            "Han Chinese",
            "Japanese",
            "Koreans",
            "Mongols",
            "Nepali",
            "Manchu",
            "Tibetans",
            "Hui",
            "Zhuang",
            "Uyghur",
        ],
        "south_asian" : [
            "Bengalis",
            "Gujarati",
            "Nepali",
            "Punjabi",
            "Hindustani",
            "Kashmiris",
            "Malayali",
            "Sindhis",
            "Sinhalese",
        ],
        "south_east_asian": [
            "Vietnamese",
            "Karen",
            "Javanese",
            "Malays",
            "Tais",
        ],
        "hispanic": [
            "Spaniards",
        ],
        "caucasian": [
            "Albanians",
            "Belarusians",
            "British",
            "Bulgarians",
            "Catalans",
            "Cornish",
            "Corsicans",
            "Croats",
            "Czechs",
            "Danes",
            "Dutch",
            "English",
            "Estonians",
            "Finns",
            "French",
            "Germans",
            "Greeks",
            "Georgians",
            "Irish",
            "Italians",
            "Hungarians",
            "Icelanders",
            "Latvians",
            "Lithuanians",
            "Norwegians",
            "Romanians",
            "Romani",
            "Russians",
            "Scottish",
            "Serbs",
            "Slovaks",
            "Poles",
            "Portuguese",
            "Swedes",
            "Welsh",
            "Slovenes",
            "Macedonians",
            "Ukrainians",
            "Moldovans",
        ],
        "middle_eastern" : [
            "Jews",
            "Kurds",
            "Persians",
            "Kazakhs",
            "Pashtuns",
            "Arabs",
            "Azerbaijanis",
            "Armenians",
            "Assyrians",
            "Uzbek",
            "Turks",
            "Turkmens",
        ]
    }
    for race, ethnicities in race_ethnicity_map.iteritems():
        race_obj = models.Trait.objects.filter(name=race, type__name='race').first()
        ethnicities = models.Trait.objects.filter(name__in=[slugify(ethnicity_label) for ethnicity_label in ethnicities])
        for ethnicity in ethnicities: 
            ethnicity.parent_type = race_obj
            ethnicity.save()
    undetermined_ethnicities = ["Acholi", 
            "Akan",
            "Afar",
            "Afrikaners",
            "Amhara",
            "Assamese",
            "Balochis",
            "Bamars",
            "Bambara",
            "Bashkirs",
            "Basques",
            "Bemba",
            "Berbers",
            "Beti-Pahuin",
            "Bosniaks",
            "Brahui",
            "Chuvash",
            "Circassians",
            "Chewa",
            "Dinka",
            "Faroese",
            "Frisians",
            "Fula",
            "Ga-Adangbe",
            "Gagauz",
            "Galician",
            "Ganda",
            "Hadiya",
            "Hausa",
            "Ibibio",
            "Igbo",
            "Ijaw",
            "Kannada",
            "Kikuyu",
            "Kongo",
            "Konkani",
            "Kyrgyz",
            "Lango",
            "Laz",
            "Luba",
            "Luo",
            "Maltese",
            "Mandinka",
            "Marathi",
            "Mongo",
            "Naga",
            "Nubians",
            "Nuer",
            "Odia",
            "Oromo",
            "Parsi",
            "Pedi",
            "Sara",
            "Sardinians",
            "Shona",
            "Soga",
            "Somalis",
            "Songhai",
            "Soninke",
            "Sotho",
            "Sundanese",
            "Sukuma",
            "Swazi",
            "Tajiks",
            "Tamils",
            "Telugu",
            "Tswana",
            "Tuaregs",
            "Volga Tatars",
            "Xhosa",
            "Yakuts",
            "Yoruba",
            "Zulu"]

