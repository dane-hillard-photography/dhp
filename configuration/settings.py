import logging
import os

from django.http import Http404
from django.utils.log import DEFAULT_LOGGING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENVIRONMENT = os.getenv('STAGE', 'dev')
IS_DEVELOPMENT = ENVIRONMENT == 'dev'
IS_STAGING = ENVIRONMENT == 'staging'
IS_PRODUCTION = ENVIRONMENT == 'production'
IS_CI = os.getenv('CI', False) == 'true'

PREPEND_WWW = IS_PRODUCTION

PROJECT_NAME = 'DHP'
PROJECT_VARIABLE_PATTERN = '_'.join((PROJECT_NAME, '{}'))


def get_env_var(var_name, default=None):
    return os.getenv(PROJECT_VARIABLE_PATTERN.format(var_name), default)


SITE_NAME = 'Dane Hillard Photography'

SECRET_KEY = get_env_var('SECRET_KEY')

DEBUG = IS_DEVELOPMENT or IS_CI

ADMINS = (
    ('Dane Hillard', 'github@danehillard.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': get_env_var('DATABASE_NAME'),
        'USER': get_env_var('DATABASE_USER'),
        'PASSWORD': get_env_var('DATABASE_PASSWORD'),
        'HOST': get_env_var('DATABASE_HOST', 'localhost'),
        'PORT': get_env_var('DATABASE_PORT', 3306),
        'CONN_MAX_AGE': 300,
        'OPTIONS': {
            'use_pure': True,
        },
    }
}

SOCIAL_MEDIA = {
    'facebook': 'danehillard',
    'instagram': 'danehillard',
    'pinterest': 'danehillard',
    'twitter': 'danehillard',
    'youtube': 'danehillard',
    'linkedin': 'danehillard',
}

LOGIN_REDIRECT_URL = '/'
ALLOWED_HOSTS = get_env_var('ALLOWED_HOSTS', '*').split(',')

TIME_ZONE = 'America/Detroit'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = False

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context_processors.template_visible_settings',
            ],
        },
    },
]

MAILCHIMP_SIGNUP_LINK = 'http://eepurl.com/bfrKM1'

TEMPLATE_VISIBLE_SETTINGS = (
    'SOCIAL_MEDIA',
    'MAILCHIMP_SIGNUP_LINK',
    'DISQUS_DOMAIN',
    'FONT_FAMILY',
    'RECAPTCHA_SITE_KEY',
)

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'logutil.middleware.request_id_middleware',
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

MIDDLEWARE.extend([
    'security.middleware.content_security_policy_middleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'seo.middleware.redirect_middleware',
    'seo.middleware.crawler_middleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
])

ROOT_URLCONF = 'configuration.urls'
WSGI_APPLICATION = 'configuration.wsgi.application'

THIRD_PARTY_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'sorl.thumbnail',
    'webpack_loader',
]

if DEBUG:
    THIRD_PARTY_APPS += [
        'debug_toolbar',
    ]

MY_APPS = [
    'blog',
    'photography',
    'home',
    'about',
    'contact',
    'branding',
    'seo',
    'security',
]

INSTALLED_APPS = THIRD_PARTY_APPS + MY_APPS

ADMIN_URL = get_env_var('ADMIN_URL', 'admin/')

EMAIL_AWS_ACCESS_KEY_ID = get_env_var('AWS_ACCESS_KEY_ID')
EMAIL_AWS_SECRET_ACCESS_KEY = get_env_var('AWS_SECRET_ACCESS_KEY')

MAILCHIMP_API_KEY = get_env_var('MAILCHIMP_API_KEY')
MAILCHIMP_LIST_ID = get_env_var('MAILCHIMP_LIST_ID')

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

LOGGING_CONFIG = None
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOGGERS = {
    '': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'django.server': DEFAULT_LOGGING['loggers']['django.server']
}
LOGGERS.update({
    app: {
        'level': LOG_LEVEL,
        'handlers': ['console'],
        'propagate': False,
    } for app in MY_APPS
})
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server']
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server']
    },
    'loggers': LOGGERS,
})

WHITELISTED_CRAWLERS = {
    'facebook': [
        'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
        'facebookexternalhit/1.1',
        'Facebot',
    ],
    'twitter': [
        'Twitterbot',
        'Twitterbot/1.0',
    ],
    'google': [
        'Googlebot',
        'Googlebot/2.1',
    ],
}

CODEMIRROR_MODE = 'xml'
CODEMIRROR_THEME = 'blackboard'

ROLLBAR = {
    'access_token': get_env_var('ROLLBAR_ACCESS_TOKEN'),
    'environment': ENVIRONMENT,
    'root': BASE_DIR,
    'exception_level_filters': [
        (Http404, 'ignored'),
    ]
}

DISQUS_DOMAIN = 'danehillard' if IS_PRODUCTION else 'danehillard-dev'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000

RECAPTCHA_SITE_KEY = get_env_var('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = get_env_var('RECAPTCHA_SECRET_KEY')

if IS_PRODUCTION or IS_STAGING:
    STATICFILES_STORAGE = 'configuration.storages.StaticStorage'
    DEFAULT_FILE_STORAGE = 'configuration.storages.MediaStorage'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

BUCKET_PREFIX = os.getenv('BUCKET_PREFIX')

MEDIA_BUCKET_NAME = f'{BUCKET_PREFIX}-media-{ENVIRONMENT}'
MEDIA_DOMAIN = f'media-{ENVIRONMENT}.danehillard.com'
MEDIA_URL = '/media/' if DEBUG else f'https://{MEDIA_DOMAIN}/'

STATIC_BUCKET_NAME = f'{BUCKET_PREFIX}-static-{ENVIRONMENT}'
STATIC_DOMAIN = f'static-{ENVIRONMENT}.danehillard.com'
STATIC_URL = '/static/' if DEBUG else f'https://{STATIC_DOMAIN}/'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_IS_GZIPPED = True

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': ['.+\.hot-update.js', '.+\.map']
    }
}
