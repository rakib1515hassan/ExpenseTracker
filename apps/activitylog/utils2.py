from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.db import models
import json
from uuid import UUID
from datetime import datetime, time
from django.utils import timezone
from decimal import Decimal

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            if obj.time() == time(0, 0): 
                return obj.strftime('%d-%m-%Y') 
            else:
                return obj.strftime('%d-%m-%Y %I:%M %p')
        elif isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, Decimal):
            print("_____________")
            print("Decimal to string", str(float(obj)))
            print("_____________")
            return str(float(obj))
        return super().default(obj)
    
    
def model_to_dict_with_nulls(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, models.ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                # Check if the field value is a queryset
                if hasattr(instance, f.name):
                    queryset = getattr(instance, f.name).all()
                    data[f.name] = list(queryset.values_list('pk', flat=True))
                else:
                    data[f.name] = []
                    
        elif isinstance(f, models.ForeignKey):
            data[f.name] = f.value_from_object(instance)

        # elif isinstance(f, models.ImageField):
            # data[f.name] = getattr(instance, f.name).url if getattr(instance, f.name) else None
        elif isinstance(f, models.ImageField):
            verbose_name = f.verbose_name if f.verbose_name else f.name
            data[verbose_name] = getattr(instance, f.name).url if getattr(instance, f.name) else None

        # elif isinstance(f, models.DateField) and getattr(instance, f.name) is not None:
            # data[f.name] = getattr(instance, f.name).strftime('%d-%m-%Y')
        # elif isinstance(f, models.DateField):
        #     value = getattr(instance, f.name)
        #     if value is not None:
        #         if isinstance(value, datetime):
        #             formatted_date = value.strftime('%d-%m-%Y %I:%M %p') if value.time() != time(0, 0) else value.strftime('%d-%m-%Y')
        #         else:
        #             formatted_date = value.strftime('%d-%m-%Y')
        #         verbose_name = f.verbose_name if f.verbose_name else f.name
        #         data[verbose_name] = formatted_date
        elif isinstance(f, models.DateTimeField) or isinstance(f, models.DateField):
            value = getattr(instance, f.name)
            if value is not None:
                # Convert to local timezone if the value is a datetime object
                if isinstance(value, datetime):
                    value = timezone.localtime(value)
                # Format the date
                formatted_date = value.strftime('%d-%m-%Y %I:%M %p') if isinstance(f, models.DateTimeField) else value.strftime('%d-%m-%Y')
                # Use verbose name if available, otherwise use field name
                verbose_name = f.verbose_name if f.verbose_name else f.name
                data[verbose_name] = formatted_date

        else:
            # Use verbose name if available, otherwise use field name
            key = str(f.verbose_name) if f.verbose_name else f.name
            data[key] = f.value_from_object(instance)

    print('----------------')
    print('Field =', {str(key): value for key, value in data.items()})
    print('----------------')
    return data