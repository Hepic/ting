from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Channel(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=20, unique=True)


class Message(models.Model):
    def __str__(self):
        return self.message_content

    def to_dict(self):
        serializable_fields = ('message_content', 'datetime_start', 'datetime_sent', 'username')
        return {key: getattr(self, key) for key in serializable_fields}

    TEXT = 'text'
    IMAGE = 'image'

    MESSAGE_TYPE = (
        (TEXT, 'text'),
        (IMAGE, 'image'),
    )

    message_content = models.TextField(max_length=2000)
    datetime_start = models.DateTimeField(default=None)
    datetime_sent = models.DateTimeField(default=None, null=True)
    typing = models.BooleanField(default=False)
    username = models.CharField(max_length=20)
    channel = models.ForeignKey(Channel)
    message_type = models.CharField(max_length=10,
                                    choices=MESSAGE_TYPE,
                                    default=TEXT)


class TingUser(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'
    OTHER = 'Other'

    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDERS, default=MALE)
    birthday = models.DateTimeField(default=None, blank=True, null=True)
    location = models.CharField(max_length=50, default=None, blank=True, null=True)
    last_used = models.DateTimeField(default=None, blank=True, null=True)

    @receiver(post_save, sender=User)
    def create_profile(sender, **kwargs):
        if kwargs['created']:
            TingUser.objects.create(user=kwargs['instance'])

    @receiver(post_save, sender=User)
    def save_profile(sender, **kwargs):
        kwargs['instance'].tinguser.save()
