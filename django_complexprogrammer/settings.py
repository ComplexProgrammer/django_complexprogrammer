"""
Django settings for django_complexprogrammer project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
# if request.device.is_mobile:
# ALLOWED_HOSTS =  ['*']
ALLOWED_HOSTS =  ['complexprogrammer.uz', 'www.complexprogrammer.uz', '10.0.2.2', 'www.complexprogrammer-dev.uz', '127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'projects',
    'whitenoise.runserver_nostatic',
    'django_extensions',
    'core',
    'tests',
    'pdf_tools',
    'markets',
    'news',
    'comments',  # Add comments app
    'blog',
    'cryptomarket',
    'site_clones',
    'ckeditor', # CKEditor config
    'ckeditor_uploader', # CKEditor media uploader
    'colorfield',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'mobiledetect.middleware.DetectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.StaticFileMiddleware',
]

ROOT_URLCONF = 'django_complexprogrammer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'django_complexprogrammer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# DATABASES = {
#     "default": {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'railway',
#         'USER': 'postgres',
#         'PASSWORD': '*24-Cf6ee13fBf-cda1ad3gFFgEdf4dd',
#         'HOST': 'monorail.proxy.rlwy.net',
#         'PORT': '49677', 
#     }
# }
# DATABASES = {
#     "default": {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'complex1_complexprogrammer',
#         'USER': 'complex1_C0mplex',
#         'PASSWORD': 'P@$$p0rtP@$$c0de',
#         'HOST': '127.0.0.200',
#         'PORT': '5432', 
#     }
# }
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

USE_L10N = True

SOLID_I18N_USE_REDIRECTS = False

LANGUAGES = (
    ('uz', _('Uzbek')),
    ('en', _('English')),
    ('tr', _('Turkish')),
    ('ru', _('Russia')),
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL='/media/'
STATICFILES_DIRS=[BASE_DIR / 'static', BASE_DIR / 'media']
STATIC_ROOT=BASE_DIR / 'staticfiles'
MEDIA_ROOT=BASE_DIR / 'media'
CKEDITOR_UPLOAD_PATH="uploads/"
# if DEBUG == True:
#     STATICFILES_DIRS=[BASE_DIR / 'static', BASE_DIR / 'media']
#     STATIC_ROOT=BASE_DIR / 'staticfiles'
#     MEDIA_ROOT=BASE_DIR / 'media'
# else:
#     STATICFILES_DIRS = (
#                         '/home/complex1/complexprogrammer.uz/django/static',
#                         '/home/complex1/complexprogrammer.uz/django/media',
#                    )
#     STATIC_ROOT = '/home/complex1/complexprogrammer.uz/django/staticfiles'
#     MEDIA_ROOT='/home/complex1/complexprogrammer.uz/django/media'



STATICFILES_FINDERS=[
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
CKEDITOR_CONFIGS = {
    'default': {
     
        'toolbar_Custom': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Youtube','Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['CodeSnippet']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'Custom',  # put selected toolbar config here
        'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        'height': 400,
        # 'width': '100%',
        'filebrowserWindowHeight': 725,
        'filebrowserWindowWidth': 940,
        'toolbarCanCollapse': True,
        'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'codesnippet',
        ]),
    }
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# APPEND_SLASH=False
GET_FILE_FORMATS = {'.mp3', '.mp4', '.zip', '.xml', 'docx', '.jpg', 'jpeg', '.csv', 'xlsx'}
UPLOAD_FOLDER_VIDEOS = STATIC_URL+'uploaded_videos/'
CARTOONIZED_FOLDER = STATIC_URL+'cartoonized_images/'
WRITE_BOX_CARTOONIZER = STATIC_URL+'white_box_cartoonizer/'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# SESSION_COOKIE_SECURE = False
# CSRF_COOKIE_SECURE = False
if DEBUG:
    SECURE_SSL_REDIRECT = False
else:
    SECURE_SSL_REDIRECT = True

COLOR_PALETTE = [
    ("#FFFFFF", "white", ),
    ("#FF0000", "red", ),
    ("#FFFF00", "yellow", ),
    ("#0000FF", "blue", ),
    ("#000000", "black", ),
]

X_FRAME_OPTIONS = 'ALLOWALL'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465  # Changed to 465 for SSL
EMAIL_USE_SSL = True  # Using SSL instead of TLS
EMAIL_USE_TLS = False  # Disable TLS when using SSL
EMAIL_HOST_USER = 'complexprogrammer@mail.ru'
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'complexprogrammer@mail.ru'
SERVER_EMAIL = 'complexprogrammer@mail.ru'
