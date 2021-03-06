from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500, handler403, handler400
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from decorator_include import decorator_include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView


from .decorators import *
from user_auth.views import *
from blog.sitemaps import *


sitemaps = {
    'static': StaticSitemap(),
    'posts': PostsSitemap(),
}

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}),
    path('robots.txt/', TemplateView.as_view(template_name='robots.txt', content_type="text/plain")),
]

urlpatterns += i18n_patterns(
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    # TODO : change secret in deployment
    path('secret/', admin.site.urls),
    path('main/', decorator_include(writeruser_required, 'base.urls')),
    path('', decorator_include(complete_oauth_profile, 'blog.urls')),
    path('auth/', include('user_auth.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    handler400 = ErrorHandler.as_view(status_code=400)
    handler403 = ErrorHandler.as_view(status_code=403)
    handler404 = ErrorHandler.as_view(status_code=404)
    # urls.E007 : defaults.server_error(request, template_name='500.html')
    handler500 = handler500