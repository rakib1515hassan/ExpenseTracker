from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Time",)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Time",)

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']


# class City(TimestampedModel):
#     city    = models.CharField(max_length=100)
#     state   = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)



