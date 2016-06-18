import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = 'DHP'
PROJECT_VARIABLE_PATTERN = '_'.join((PROJECT_NAME, '{}'))


def get_env_var(var_name, default=None):
    return os.getenv(PROJECT_VARIABLE_PATTERN.format(var_name), default)

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
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'seo.middleware.RedirectMiddleware',
    'seo.middleware.CrawlerMiddleware',
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
)

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
    'django_nose',
    'compressor',
    'webmention',
]

MY_APPS = [
    'blog',
    'photography',
    'home',
    'about',
    'contact',
    'branding',
    'seo',
]

INSTALLED_APPS = THIRD_PARTY_APPS + MY_APPS

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache' if not DEBUG else 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': get_env_var('MEMCACHED_ENDPOINT', '127.0.0.1:11211'),
    }
}

CACHE_MIDDLEWARE_SECONDS = 3600
CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_NAME.lower()

ADMIN_URL = get_env_var('ADMIN_URL', r'^admin/')

COMPRESS_CSS_FILTERS = (
    'compressor.filters.cssmin.CSSMinFilter',
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

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner' 

NOSE_ARGS = [
    '-d',
    '--quiet',
    '--with-fixture-bundling',
    '--with-coverage',
    '--cover-package=.',
    '--cover-erase',
]

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
    'access_token': 'ce60f2254ab046f5917b9cea7b467068',
    'environment': 'development' if DEBUG else 'production',
    'root': BASE_DIR,
}

DISQUS_DOMAIN = 'danehillard-dev' if DEBUG else 'danehillard'
