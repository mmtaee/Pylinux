from django.core.signals import request_started
from django.dispatch import receiver
from django.urls import reverse_lazy

from datetime import datetime

from .models import *

@receiver(request_started)
def site_requests(sender, environ, **kwargs):
    host = environ['HTTP_HOST']
    path = environ['PATH_INFO']
    request_url = host + path
    blog_url = host + str(reverse_lazy('blog:blog'))
    home_url = host + "/"

    if request_url == home_url:
        home, create = HomeRequest.objects.get_or_create(
            date__month=current_month,
            date__year=current_year,
            )
        home.num +=1
        home.save()

    if request_url == blog_url:
        blog, create = BlogRequest.objects.get_or_create(date=datetime.today())
        blog.num += 1
        blog.save()