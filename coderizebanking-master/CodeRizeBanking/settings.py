
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@9tk*mmuzj6im*8ibyh86y775#+89_ta&$_kezf(pnp#j0y0*o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "cib.localhost",
    # "Fruitly.cib.localhost",
    # "FruitBet.cib.localhost",
    # "CodeRize.cib.localhost",
    'cib.fruitly.in',
    'coderize.cib.fruitly.in',
    'fruitbet.cib.fruitly.in',
    'fruitly.cib.fruitly.in',
    '209.182.234.23'
]


# Application definition

SHARED_APPS = [
    'django_tenants',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sslserver',
    'rest_framework',
    'corsheaders',
    'Customers',
    'CIBPayment',
    'accounts',
    'rest_framework.authtoken',

]

TENANT_APPS = [
    'django.contrib.contenttypes',
    # 'CIBPayment',
]

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

MIDDLEWARE = [
    'django_tenants.middleware.TenantMiddleware',  # Use TenantMiddleware for subdomain-based tenancy
    'django_tenants.middleware.TenantSubfolderMiddleware',
    'django_tenants.middleware.subfolder.TenantSubfolderMiddleware',

    'django_tenants.middleware.main.TenantMainMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
    
ROOT_URLCONF = 'CodeRizeBanking.urls'
PUBLIC_SCHEMA_URLCONF = 'CodeRizeBanking.urls'
AUTH_USER_MODEL = 'accounts.CustomUser'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'CodeRizeBanking.wsgi.application'

# Database
if os.environ.get('LIFECYCLE') == 'LIVE':
    db_name = 'fruitlycoderize'
    DEBUG = False
else:
    db_name = 'fruitlycoderize'
    DEBUG = True

try:
    from Logger import logger

    logger.info(f"Using database: {db_name}")
except:
    pass
print(f"Using database: {db_name}")

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': "fruitlycoderize",
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'Sanket@123',
    }
}
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TENANT_MODEL = "Customers.Client"  # app.Model
TENANT_DOMAIN_MODEL = "Customers.Domain"  # app.Model
SHOW_PUBLIC_IF_NO_TENANT_FOUND = True
TENANT_SUBFOLDER_PREFIX = "clients"

log_file_path = os.path.join(Path(__file__).parent.parent, 'Logger', 'django_logs', 'debug.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': log_file_path,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
            'propagate': True,
        },
    },
}

CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = [
    'https://cib.fruitly.in',
    'https://fruitbet.cib.fruitly.in/',
    'https://coderize.cib.fruitly.in/',
    'https://fruitly.cib.fruitly.in/',
    'http://localhost',  
    'https://products.coderize.in',
    # 'https://products.coderize.in/chhaya/',
    'http://localhost:4200',
]


CORS_ALLOWED_ORIGINS = [
    'https://products.coderize.in',
    # 'https://products.coderize.in/chhaya/',
    'http://localhost:4200',   
]

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'PUT',
    'PATCH', 
    'DELETE',
    'OPTIONS',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# settings.py

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.coderize.in'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sanket.lodhe@coderize.in'
EMAIL_HOST_PASSWORD = 'Sanket@4890'
DEFAULT_FROM_EMAIL = 'sanket.lodhe@coderize.in'

