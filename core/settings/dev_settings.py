from .base_settings import *

SECRET_KEY = '$a!0kd$g6wsdfsddfsdfskkyy9837294879294289oishsdfs)&h1&6ev%hw*2igs-kg9*s_xbdm6(u5!_1r-1z9x'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gransoft_farms',
        'USER': 'daniel',
        'PASSWORD': 'daniel',
        'HOST': 'localhost',
        'PORT': 5433
    }
}
