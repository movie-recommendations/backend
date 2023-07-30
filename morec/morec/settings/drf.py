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
JWT_REFRESH_TTL = 3600 * 24 * 7  # время жизни refresh токена в секундах (неделя)


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_NAME = "MoRec"
HOST = "http://127.0.0.1:8000"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = "your@gmail.com"
EMAIL_HOST_PASSWORD = "password"
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
