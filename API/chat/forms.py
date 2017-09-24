import time

from django import forms
from .models import Message
from django.contrib.auth.models import User
from .utils import timestamp_to_datetime, datetime_to_timestamp
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class MessageForm(forms.Form):
    message_content = forms.CharField(widget=forms.Textarea)
    typing = forms.BooleanField(required=False)
    message_type = forms.CharField(widget=forms.Textarea)


class MessageCreationForm(MessageForm):
    username = forms.CharField(max_length=20)
    datetime_start = forms.IntegerField()

    def clean_datetime_start(self):
        now = int(round(time.time() * 1000))
        timestamp = int(self.data['datetime_start'])
        if now < timestamp:
            timestamp = now

        self.cleaned_data['datetime_start'] = timestamp_to_datetime(timestamp)

    def save(self):
        self.clean_datetime_start()

        message = Message.objects.create(channel=self.channel, **self.cleaned_data)

        if not message.typing:
            message.datetime_sent = message.datetime_start
            message.save()

        return message


class MessagePatchForm(MessageForm):
    datetime_sent = forms.IntegerField()

    def save(self, message):
        timestamp_start = datetime_to_timestamp(message.datetime_start)
        timestamp_sent = int(self.cleaned_data['datetime_sent'])

        if timestamp_sent < timestamp_start:
            timestamp_sent = timestamp_start

        message.datetime_sent = timestamp_to_datetime(timestamp_sent)
        message.message_content = self.cleaned_data['message_content']
        message.typing = self.cleaned_data.get('typing', False)

        message.save()


class SessionForm(AuthenticationForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, strip=False)
    _response = None

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is None:
            raise forms.ValidationError(
                'invalid_username',
                code='invalid_username'
           )

        try:
            user = User.objects.get(username=username)

            if user.has_usable_password():
                if password is None:
                    raise forms.ValidationError(
                        'password_required',
                        code='password_required'
                    )

                auth = authenticate(username=username, password=password)

                if auth is None:
                    raise forms.ValidationError(
                        'wrong_password',
                        code='wrong_password'
                    )

                if auth.is_active:
                    self._response = 'Authenticate'
                    return

            now = int(round(time.time() * 1000))
            seconds = (now - datetime_to_timestamp(user.tinguser.last_used)) / 1000

            if seconds > 86400:
                self._response = 'Unreserved'
                return

            raise forms.ValidationError(
                'username_reserved',
                code='username_reserved'
            )

        except User.DoesNotExist:
            if password is not None:
                raise forms.ValidationError(
                    'password_set',
                    code='password_set'
                )

            self._response = 'Unreserved'

    def save(self):
        username = self.cleaned_data.get('username')

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            user = User.objects.create_user(
                username = username
            )

        now = int(round(time.time() * 1000))
        current_datetime = timestamp_to_datetime(now)

        user.tinguser.last_used = current_datetime
        user.save()

    def getResponse(self):
        return self._response
