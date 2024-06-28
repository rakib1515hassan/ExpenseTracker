from django.contrib import admin
from apps.activitylog.models import ActivityLog


# Register your models here.
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):

    list_display = ['id', 'actor', 'action_type', 'action_time', 'status']
