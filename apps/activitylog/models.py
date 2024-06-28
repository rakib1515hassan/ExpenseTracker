from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class ActivityLog(models.Model):
    class ActionTypes(models.TextChoices):
        CREATE = 'Create', 'create'
        READ   = 'Read'  , 'read'
        UPDATE = 'Update', 'update'
        DELETE = 'Delete', 'delete'
        LOGIN  = 'Login' , 'login'
        LOGOUT = 'Logout', 'logout'
        LOGIN_FAILED = 'Login Failed', 'login failed'

    class ActionStatus(models.TextChoices):
        SUCCESS = 'Success', 'success'
        FAILED  = 'Failed' , 'failed'

    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    action_type = models.CharField(choices=ActionTypes, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)

    remarks = models.TextField(null=True, blank=True)
    status  = models.CharField(choices=ActionStatus, max_length=7, default=ActionStatus.SUCCESS)
    data    = models.JSONField(default=dict)

    # object_id = models.PositiveIntegerField(blank=True, null=True)
    object_id = models.CharField(max_length=50, blank=True, null=True)

    # for generic relations
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.action_type} by {self.actor} on {self.action_time}"
