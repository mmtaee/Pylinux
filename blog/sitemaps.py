from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from base.models import *


class StaticSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['home', 'blog', 'search']

    def location(self, item):
        return reverse("blog:" + item)


class PostsSitemap(Sitemap):
    priority = 0.5
    changefreq = "daily"

    def items(self):
        posts = Post.objects.all().order_by('-title')
        return posts

    def location(self, obj):
        return obj.get_absolute_url_blog()

    def lastmod(self, obj):
        return obj.last_update
