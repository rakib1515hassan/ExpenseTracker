from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from django.db import models
import json
from uuid import UUID
from datetime import datetime, time, date
# import datetime
from django.utils import timezone
from django.utils.text import camel_case_to_spaces
from django.core.exceptions import FieldDoesNotExist
from copy import deepcopy
import json 

## Custom Import
from apps.activitylog.models import ActivityLog
from apps.activitylog.utils2 import CustomJSONEncoder, model_to_dict_with_nulls
from decimal import Decimal

"""NOTE:- This is create log
    Create Log
"""
def create_log(actor, model_instance, instance_data=None, remarks=None):
    content_type = ContentType.objects.get_for_model(model_instance)
    model_name = content_type.model.split('.')[-1]
    object_id = model_instance.pk

    # if instance_data is None:
    #     instance_data = serialize('json', [model_instance])

    print("---------------------")
    # print(f"Model = {content_type}, Model Name ={model_name} Id = {object_id}")

    # print("--------------")
    # print("Model Data = ", model_instance.__dict__)
    # print("--------------")

    if instance_data is None:
        instance_data_dict = model_to_dict_with_nulls(model_instance)

        # Convert UUID objects to strings and datetime objects to ISO format
        instance_data_dict = {
            key: CustomJSONEncoder().default(value) if isinstance(value, (UUID, datetime)) else value
            for key, value in instance_data_dict.items()
        }

        # Convert Decimal objects to strings
        instance_data_dict = {
            key: str(value) if isinstance(value, Decimal) else value
            for key, value in instance_data_dict.items()
        }

        instance_data = {
            'model': f"{str(content_type.app_label)}.{str(content_type.model)}",
            'pk': str(model_instance.pk),
            'fields': instance_data_dict
        }

    print(f"Data = {instance_data}")
    print("---------------------")
    try:
        ActivityLog.objects.create(
            action_type=ActivityLog.ActionTypes.CREATE,
            action_time=datetime.now(),
            status=ActivityLog.ActionStatus.SUCCESS,

            content_type=content_type,
            object_id=object_id,

            actor=actor,
            data=instance_data,
            remarks=remarks,
        )
    except Exception as e:
        print("+++++++++++++++++++")
        print(f"Error occurred while creating log: {str(e)}")
        print("+++++++++++++++++++")



"""NOTE:- This is update log
    Update Log
"""
def update_log(actor, model_instance, instance_data=None, remarks=None, changes_data = None):
    content_type = ContentType.objects.get_for_model(model_instance)
    model_name = content_type.model.split('.')[-1]
    object_id = model_instance.pk

    # if instance_data is None:
    #     instance_data = serialize('json', [model_instance])

    # print("--------------")
    # print(f"Model = {content_type}, Model Name ={model_name} Id = {object_id}")
    # print("Model Data = ", model_instance.__dict__)
    # print("--------------")

    # Format datetime values in changes_data dictionary
    # if changes_data:
    #     for field_name, data in changes_data.items():
    #         old_value = data.get('old')
    #         new_value = data.get('new')
    #         # Format old and new datetime values if present
    #         if isinstance(old_value, datetime):
    #             old_value = old_value.strftime('%d-%m-%Y %I:%M %p') if old_value.time() != datetime.min.time() else old_value.strftime('%d-%m-%Y')
    #         if isinstance(new_value, datetime):
    #             new_value = new_value.strftime('%d-%m-%Y %I:%M %p') if new_value.time() != datetime.min.time() else new_value.strftime('%d-%m-%Y')
    #         # Update the changes_data dictionary
    #         changes_data[field_name]['old'] = old_value
    #         changes_data[field_name]['new'] = new_value

    if changes_data:
        changes_data_copy = deepcopy(changes_data)
        for field_name, data in changes_data_copy.items():
            try:
                field = model_instance._meta.get_field(field_name)
                verbose_name = field.verbose_name if field.verbose_name else camel_case_to_spaces(field_name)
            except FieldDoesNotExist:
                verbose_name = camel_case_to_spaces(field_name)

            old_value = data.get('old')
            new_value = data.get('new')

            # print("---------------")
            # print(f"Field Name= {verbose_name}, Old value: {old_value}, new value:{new_value}")
            # print("changes_data =", changes_data)
            # print("---------------")

            # Convert datetime.date objects to strings
            if isinstance(old_value, datetime):
                old_value = old_value.strftime('%d-%m-%Y %I:%M %p') if old_value.time() != datetime.min.time() else old_value.strftime('%d-%m-%Y')
            elif isinstance(old_value, date):
                old_value = old_value.strftime('%d-%m-%Y')
            elif old_value is not None and not isinstance(old_value, str):
                old_value = str(old_value)

            if isinstance(new_value, datetime):
                new_value = new_value.strftime('%d-%m-%Y %I:%M %p') if new_value.time() != datetime.min.time() else new_value.strftime('%d-%m-%Y')
            elif isinstance(new_value, date):
                new_value = new_value.strftime('%d-%m-%Y')
            elif new_value is not None and not isinstance(new_value, str):
                new_value = str(new_value)

            # Convert Decimal objects to strings
            if isinstance(old_value, Decimal):
                old_value = str(old_value)
            if isinstance(new_value, Decimal):
                new_value = str(new_value)

            # Update the changes_data dictionary with verbose field name
            changes_data[verbose_name] = {'old': old_value, 'new': new_value}
            # Remove the original field name entry
            del changes_data[field_name]

    if instance_data is None:
        instance_data_dict = model_to_dict_with_nulls(model_instance)
        # Convert UUID objects to strings and datetime objects to ISO format
        instance_data_dict = {
            key: CustomJSONEncoder().default(value) if isinstance(value, (UUID, datetime)) else value
            for key, value in instance_data_dict.items()
        }
        # Convert Decimal objects to strings
        instance_data_dict = {
            key: str(value) if isinstance(value, Decimal) else value
            for key, value in instance_data_dict.items()
        }
        instance_data = {
            'model': f"{str(content_type.app_label)}.{str(content_type.model)}",
            'pk': str(model_instance.pk),
            'fields': instance_data_dict,
            'changes': changes_data,
        }
        

    print("_____________________________")
    print("Final Data = ", instance_data)
    print("_____________________________")

    try:
        ActivityLog.objects.create(
            action_type = ActivityLog.ActionTypes.UPDATE,
            action_time = datetime.now(),
            status = ActivityLog.ActionStatus.SUCCESS,

            object_id = object_id,
            content_type = content_type,

            actor = actor,
            data  = instance_data,
            remarks = remarks,
        )
    except Exception as e:
        print("+++++++++++++++++++")
        print(f"Error occurred while updating log: {str(e)}")
        print("+++++++++++++++++++")





"""NOTE:- This is delete log
    Delete Log
"""
def delete_log(actor, model_instance, instance_data=None, remarks=None):

    content_type = ContentType.objects.get_for_model(model_instance)
    model_name = content_type.model.split('.')[-1]
    object_id = model_instance.pk

    # if instance_data is None:
    #     instance_data = serialize('json', [model_instance])

    print("---------------------")
    print(f"Model = {content_type}, Model Name ={model_name} Id = {object_id}")

    # print("--------------")
    # print("Model Data = ", model_instance.__dict__)
    # print("--------------")

    if instance_data is None:
        instance_data_dict = model_to_dict_with_nulls(model_instance)
        # Convert UUID objects to strings and datetime objects to ISO format
        instance_data_dict = {
            key: CustomJSONEncoder().default(value) if isinstance(value, (UUID, datetime)) else value
            for key, value in instance_data_dict.items()
        }
        # Convert Decimal objects to strings
        instance_data_dict = {
            key: str(value) if isinstance(value, Decimal) else value
            for key, value in instance_data_dict.items()
        }
        instance_data = {
            'model': f"{str(content_type.app_label)}.{str(content_type.model)}",
            'pk': str(model_instance.pk),
            'fields': instance_data_dict
        }

    print(f"Data = {instance_data}")
    print("---------------------")

    try:
        ActivityLog.objects.create(
            action_type = ActivityLog.ActionTypes.DELETE,
            action_time = datetime.now(),
            status = ActivityLog.ActionStatus.SUCCESS,

            object_id = object_id,
            content_type = content_type,

            actor = actor,
            data  = instance_data,
            remarks = remarks,
        )
    except Exception as e:
        print("+++++++++++++++++++")
        print(f"Error occurred while deleting log: {str(e)}")
        print("+++++++++++++++++++")




    


    