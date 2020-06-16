from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend

class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, **kwargs):
        email = kwargs['username'].lower()  # If you made email case insensitive add lower()
        password = kwargs['password']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.is_active and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
