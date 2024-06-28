from django.urls import path 

from apis.v1.auth import views

urlpatterns = [ 
    path('user-registration/', views.UserRegistrationView.as_view()), 


    # path('', AuthView.as_view(), name='list'), 
    # path('<int:pk>/', AuthView.as_view(), name='details'), 
] 
