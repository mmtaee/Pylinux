from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from user_auth.models import *

class EmailBackend(ModelBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

backend = EmailBackend()
