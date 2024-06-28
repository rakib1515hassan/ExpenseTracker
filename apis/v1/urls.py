from django.urls import path, include

urlpatterns = [
    path('auth/', include('apis.v1.auth.urls')),
]