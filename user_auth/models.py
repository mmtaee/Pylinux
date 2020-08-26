from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from pylinux.managers import *


class User(AbstractUser):
    bio = models.TextField(_("bio"), max_length=500, blank=True)
    image = models.ImageField(upload_to="user_image/", default='/user.jpg', null=True)
    email = models.EmailField(
        verbose_name=_('email'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=150, verbose_name='username', null=True, blank=True)
    is_writer = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    whatsapp = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    gitlab = models.URLField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if not self.username:
            return self.email
        return self.username
