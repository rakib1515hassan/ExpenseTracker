from django.urls import path
from apps.auth import views

app_name = 'auth'


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegistrationView.as_view(), name='registration'),   
    # path('restrict/', views.RestrictedView.as_view(), name='restrict'), 


    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),

    # path(
    #     'permission-update/<uuid:pk>/', 
    #     views.PermissionUpdateView.as_view(), 
    #     name='permission-update'
    # ),
]