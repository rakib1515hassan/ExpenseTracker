from django.urls import path
from apps.activitylog import views

app_name = 'activitylog'


urlpatterns = [
    path('list/', views.ActivityLogListView.as_view(), name='activity_log_list'),
    path('data/<int:pk>/', views.ActivityLogDetailsView.as_view(), name='activity_log_data'),
]