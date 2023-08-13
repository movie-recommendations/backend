import os

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.backends.JWTAuthentication',
    ],
}


JWT_REGISTRATION_TTL = 3600  # время жизни токена для регистрации в секундах (1 час)
JWT_ACCESS_TTL = 3600 * 24 * 7  # время жизни access токена в секундах (неделя)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SITE_NAME = os.environ.get('SITE_NAME', 'http://localhost')
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
