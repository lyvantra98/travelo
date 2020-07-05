import os
import pymysql
import smtplib
import django_heroku

pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2s3w=fxkk(j80cc=a!%h3#2r4b$igh=&mar*k%&#edgq0-&f5w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['travelo.herokuapp.com']

# Activate Django-Heroku.
django_heroku.settings(locals())

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'sass_processor',
    'import_export',
    'paypal.standard.ipn',
    'django.contrib.humanize',
    'crispy_forms',
    'tour',
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'tourtravel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'tourtravel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'travelo',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS =[
    'social_core.backends.open_id.OpenIdAuth',
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'tour.backends.EmailOrUsernameModelBackend',
]
# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT = 'static/'

# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(PROJECT_ROOT, 'static'),
# )
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Django Sass
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR,'static')

#Configuring a SMTP Email Service
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'tealy123321@gmail.com'
EMAIL_HOST_PASSWORD = 'deocomatkhau'
EMAIL_USE_TLS = True
# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
SOCIAL_AUTH_FACEBOOK_KEY = '1001993430216008'
SOCIAL_AUTH_FACEBOOK_SECRET = '4fb679f00d6c40d3ae10940d786a479d'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY= '274123049970-9tfgcmb43136gqalv12phkqu7j0cq8on.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'v37EHlo91DpBJ3tfP-ggWjat'
PAYPAL_RECEIVER_EMAIL = 'sb-501eq2592178@business.example.com'
PAYPAL_TEST = True
STRIPE_PUBLISHABLE_KEY = 'pk_test_51H40eYE93EuEbUzYUWrGQrP26SpB93GANQk36A6mJ0xVzILaoJCamwzhEtREoPFE3tSXRopBHwYUbsxi1mNEqNZT007Mzvoczr'
STRIPE_SECRET_KEY = 'sk_test_51H40eYE93EuEbUzYEvtpWapup8Ukh1AMw3hgWIUYTfHpYGiZdvetDcjaO3v8HdVuPNYoUyN3K2gc8JzCT0mPRo8N00qvNnWPvU'
