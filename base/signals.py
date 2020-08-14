from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import *
from user_auth.models import *


@receiver(post_delete, sender=Post)
def photo_delete_handler(sender, **kwargs):
    instance = kwargs['instance']
    if instance:
        storage, path = instance.image.storage, instance.image.path
        storage.delete(path)