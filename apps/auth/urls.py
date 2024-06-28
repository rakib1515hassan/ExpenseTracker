from django.urls import path
from apps.auth import views

app_name = 'auth'


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('restrict/', views.RestrictedView.as_view(), name='restrict'), 


    path('password-change/', views.ChangePasswordView.as_view(), name='password-change'),
]