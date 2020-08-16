from django.db.models.signals import post_save, post_delete
from django.contrib.sitemaps import ping_google
from django.dispatch import receiver

from .models import *
from user_auth.models import *

@receiver(post_delete, sender=Post)
def photo_delete_handler(sender, **kwargs):
    instance = kwargs['instance']
    if instance:
        storage, path = instance.image.storage, instance.image.path
        storage.delete(path)


@receiver(post_delete, sender=Post)
@receiver(post_save, sender=Post)
def ping_google_sitemap(sender, **kwargs):
    try :
        ping_google(
            sitemap_url="/sitemap.xml",
            ping_url = "",
            sitemap_uses_https = True
            )
    except Exception as error:
        with open ("CEO_log.txt" , 'a') as f:
            text = str(error) + "\n"
            f.write(text)
