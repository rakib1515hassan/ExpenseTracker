


## Django Rest Framework
REST_FRAMEWORK = {

    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # 'DEFAULT_FILTER_BACKENDS': [
    #         'django_filters.rest_framework.DjangoFilterBackend'
    #     ],

}