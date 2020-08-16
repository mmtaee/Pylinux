from django.utils.translation import gettext_lazy as _
import os
from decouple import config, Csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # extras :
    'django_celery_results',
    'jalali_date',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'social_django',
    'admin_honeypot',
    'django.contrib.sitemaps',
    # apps :
    'user_auth.apps.UserAuthConfig',
    'base.apps.BaseConfig',
    'blog.apps.BlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.email.EmailAuth',
    'pylinux.backends.EmailBackend'
)


ROOT_URLCONF = 'pylinux.urls'

AUTH_USER_MODEL = 'user_auth.User'

SOCIAL_AUTH_RAISE_EXCEPTIONS = False

SOCIAL_AUTH_LOGIN_ERROR_URL = '/auth/login/'

SOCIAL_AUTH_LOGIN_URL = '/oauth/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]

SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

SOCIAL_AUTH_USER_MODEL = 'user_auth.User'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'pylinux.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fa'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )

LANGUAGES = (('fa', _('Persian')),
            #  ('en', _('English')),
             )

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]

else:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%Y/%m/%d',
        'datetime': '%H:%M:%S _ %Y/%m/%d',
    },
    'Static': {
        'js': [
            'admin/js/django_jalali.min.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

CELERY_RESULT_BACKEND = 'django-db'

CELERY_CACHE_BACKEND = 'default'

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'

CELERY_ACCEPT_CONTENT = ['json']

CELERY_TASKS_SERIALIZER = 'json'

CELERY_STORE_ERRORS_EVEN_IF_IGNORED = True

EMAIL_HOST = config('EMAIL_HOST')

EMAIL_PORT = config('EMAIL_PORT', cast=int)

EMAIL_HOST_USER = config('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = True

CKEDITOR_UPLOAD_PATH = 'ckeditor/'

CKEDITOR_CONFIGS = {
    'message': {
        'toolbar': [
            [
                'NumberedList',
                'BulletedList',
                '-',
                'Outdent',
                'Indent',
                '-',
                'Blockquote',
                '-',
                'JustifyLeft',
                'JustifyCenter',
                'JustifyRight',
                'JustifyBlock',
                '-',
                'BidiLtr',
                'BidiRtl',
            ],
            ['Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat'],
            ['TextColor', 'BGColor'],
            [
                'Link',
                'Unlink',
                'Anchor',
                'ShowBlocks',
                'CodeSnippet',
            ],
        ],
        'height':
        '200px',
        'width':
        '100%',
        'extraPlugins':
        ','.join([
            'codesnippet',
        ]),
        'font_names':
        'BNazanin; Bkoodak;',
    },
    'comment': {
        'toolbar': [
            [
                'NumberedList',
                'BulletedList',
                '-',
                'Outdent',
                'Indent',
                '-',
                'Blockquote',
                '-',
                'JustifyLeft',
                'JustifyCenter',
                'JustifyRight',
                'JustifyBlock',
                '-',
                'BidiLtr',
                'BidiRtl',
            ],
            ['Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat'],
            ['TextColor', 'BGColor'],
            [
                'Link',
                'Unlink',
                'Anchor',
                'ShowBlocks',
                'CodeSnippet',
            ],
        ],
        'height':
        '300px',
        'width':
        '900px',
        'extraPlugins':
        ','.join([
            'codesnippet',
        ]),
        'font_names':
        'BNazanin; Bkoodak;',
    },
    'default': {
        'toolbar_create_post': [
            [
                'NumberedList',
                'BulletedList',
                '-',
                'Outdent',
                'Indent',
                '-',
                'Blockquote',
                '-',
                'JustifyLeft',
                'JustifyCenter',
                'JustifyRight',
                'JustifyBlock',
                '-',
                'BidiLtr',
                'BidiRtl',
            ],
            ['Styles', 'Format', 'FontSize', 'Font'],
            ['TextColor', 'BGColor'],
            [
                'Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                'Superscript', '-', 'RemoveFormat'
            ],
            [
                'Link',
                'Unlink',
                'Anchor',
            ],
            [
                'Image',
                'Table',
                'HorizontalRule',
                'Smiley',
                'SpecialChar',
                'PageBreak',
            ],
            [
                'Maximize',
                'ShowBlocks',
                'CreateDiv',
                'CodeSnippet',
                'Preview',
            ],
        ],
        'toolbar':
        'create_post',
        'height':
        '200px',
        'width':
        '100%',
        'tabSpaces':
        4,
        'extraPlugins':
        ','.join([
            'uploadimage', 'div', 'autolink', 'autoembed', 'embedsemantic',
            'autogrow', 'widget', 'lineutils', 'clipboard', 'dialog',
            'dialogui', 'elementspath', 'codesnippet'
        ]),
        'font_names':
        'BNazanin; Bkoodak;',
    }
}

RECAPTCHA_SITE_KEY = config('RECAPTCHA_SITE_KEY')

RECAPTCHA_SECRET_KEY = config('RECAPTCHA_SECRET_KEY')

RECAPTCHA_SITE_KEY_V2 = config('RECAPTCHA_SITE_KEY_V2')

RECAPTCHA_SECRET_KEY_V2 = config('RECAPTCHA_SECRET_KEY_V2')

SOCIAL_AUTH_GITHUB_KEY = config('SOCIAL_AUTH_GITHUB_KEY')

SOCIAL_AUTH_GITHUB_SECRET = config('SOCIAL_AUTH_GITHUB_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')