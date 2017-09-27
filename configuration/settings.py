import os
from django.http import Http404

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = 'DHP'
PROJECT_VARIABLE_PATTERN = '_'.join((PROJECT_NAME, '{}'))


def get_env_var(var_name, default=None):
    return os.getenv(PROJECT_VARIABLE_PATTERN.format(var_name), default)


SITE_NAME = 'Dane Hillard Photography'

SECRET_KEY = get_env_var('SECRET_KEY')

DEBUG = get_env_var('DEBUG', False) == 'TRUE'

ADMINS = (
    ('Dane Hillard', 'github@danehillard.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_env_var('DATABASE_NAME'),
        'USER': get_env_var('DATABASE_USER'),
        'PASSWORD': get_env_var('DATABASE_PASSWORD'),
        'HOST': get_env_var('DATABASE_HOST', 'localhost'),
        'PORT': get_env_var('DATABASE_PORT', 3306),
        'CONN_MAX_AGE': 300,
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

STATIC_ROOT = os.path.join(BASE_DIR, get_env_var('STATIC_ROOT', 'static'))
STATIC_URL = get_env_var('STATIC_URL', '/static/')
MEDIA_ROOT = os.path.join(BASE_DIR, get_env_var('MEDIA_ROOT', 'media'))
MEDIA_URL = get_env_var('MEDIA_URL', '/media/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
    os.path.join(BASE_DIR, 'node_modules'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
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

THE_MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'logutil.middleware.RequestIdMiddleware',
]

if DEBUG:
    THE_MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

THE_MIDDLEWARE_CLASSES.extend([
    'security.middleware.ContentSecurityPolicyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'seo.middleware.RedirectMiddleware',
    'seo.middleware.CrawlerMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
])

MIDDLEWARE_CLASSES = tuple(THE_MIDDLEWARE_CLASSES)

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
    'compressor',
    'webmention',
    'sorl.thumbnail',
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

cache_backend = 'django.core.cache.backends.memcached.MemcachedCache'

if DEBUG:
    cache_backend = 'django.core.cache.backends.dummy.DummyCache'

CACHES = {
    'default': {
        'BACKEND': cache_backend,
        'LOCATION': get_env_var('MEMCACHED_ENDPOINT', '127.0.0.1:11211'),
    }
}

CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_NAME.lower()

ADMIN_URL = get_env_var('ADMIN_URL', r'^admin/')

COMPRESS_CSS_FILTERS = (
    'compressor.filters.cssmin.CSSMinFilter',
    'compressor.filters.css_default.CssAbsoluteFilter',
)

COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'sass {infile} {outfile}'),
)

COMPRESS_OUTPUT_DIR = ''

AWS_ACCESS_KEY_ID = get_env_var('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_env_var('AWS_SECRET_ACCESS_KEY')

MAILCHIMP_API_KEY = get_env_var('MAILCHIMP_API_KEY')
MAILCHIMP_LIST_ID = get_env_var('MAILCHIMP_LIST_ID')

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': "%(asctime)s|%(levelname)s|%(name)s|%(message)s",
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
    },
    'loggers': {
        app: {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        } for app in MY_APPS
    },
}

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
    'environment': 'development' if DEBUG else 'production',
    'root': BASE_DIR,
    'exception_level_filters': [
        (Http404, 'ignored'),
    ]
}

DISQUS_DOMAIN = 'danehillard-dev' if DEBUG else 'danehillard'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000

RECAPTCHA_SITE_KEY = get_env_var('RECAPTCHA_SITE_KEY')
RECAPTCHA_SECRET_KEY = get_env_var('RECAPTCHA_SECRET_KEY')
