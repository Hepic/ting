from chat.tests.common import *
from django.contrib.auth.models import User
from chat.models import TingUser

NOW = timestamp_to_datetime(int(round(time.time() * 1000)))

def create_user(username, password=None, email='default@default.com', gender='Male', birthday=NOW, location='Somewhere', last_used=NOW):
    if password is None:
        user = User.objects.create_user(
            username=username,
            email=email
        )
    else:
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

    user.tinguser.gender = gender
    user.tinguser.birthday = birthday
    user.tinguser.location = location
    user.tinguser.last_used = last_used

    user.save()
    return user
