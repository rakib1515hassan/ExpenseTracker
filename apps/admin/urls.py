from django.urls import path
from apps.admin import views

app_name = 'admins'


urlpatterns = [
    path('create/', views.AdminCreateView.as_view(), name='admin_create'),
    path('list/',   views.AdminListView.as_view(),   name='admin_list'),
    path('delete/', views.AdminDeleteView.as_view(), name='admin_delete'),
    path('details/<uuid:pk>/', views.AdminDetailsView.as_view(), name='admin_details'),
    path('update/<uuid:pk>/',  views.AdminUpdateView.as_view(), name='admin_update'),

    path(
        'permission-update/<uuid:pk>/', 
        views.PermissionUpdateView.as_view(), 
        name='permission-update'
    ),
]