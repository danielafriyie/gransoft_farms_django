from .base_settings import *

SECRET_KEY = '$a!0kd$g6wsdfsddfsdfskkyy9837294879294289oishsdfs)&h1&6ev%hw*2igs-kg9*s_xbdm6(u5!_1r-1z9x'
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(BASE_DIR, 'server_config.cnf'),
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        },
    }
}
