from config.env import env




## Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = env('EMAIL_HOST', default='localhost')
EMAIL_PORT = env('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=False, cast=bool)

EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')


EMAIL_USE_SSL = env('EMAIL_USE_SSL')
# EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'library@texon.ltd'