from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.sessions.models import Session
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.utils import timezone

from django.db.models import Q, Count, F
from django.db.models.functions import ExtractMonth, ExtractYear

from django.http import HttpRequest, HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ValidationError, PermissionDenied

from datetime import datetime, timedelta
from random import randint

from django.views import View
from django.views import generic
import json

## Custom 
from config.permission import is_superuser_or_staff, is_superadmin
from apps.core.utils2 import CustomPaginator, ExcelDataDownload
from apps.activitylog.models import ActivityLog

"""
    ActivityLog List
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class ActivityLogListView(View, LoginRequiredMixin):
    template_name = "activitylog/list.html"
    obj_per_page = 10

    def get_queryset(self):
        queryset = ActivityLog.objects.all().order_by('-action_time')
        return queryset


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        ## NOTE:- Filter values from the GET parameters
        # user_type   = request.GET.get('user_type', '')
        # is_verified = request.GET.get('is_verified', '')
        # is_active   = request.GET.get('is_active', '')
        # created_at  = request.GET.get('created_at', '')

        # # print("----------------------")
        # # print("user_type   = ", user_type)
        # # print("is_verified = ", is_verified)
        # # print("is_active   = ", is_active)
        # # print("created_at  = ", created_at)
        # # print("----------------------")

        # if user_type:
        #     users = users.filter(user_type=user_type)
        # if is_verified != '':
        #     users = users.filter(is_verified=bool(int(is_verified)))
        # if is_active != '':
        #     users = users.filter(is_active=bool(int(is_active)))

        # if created_at != '':
        #     if 'to' in created_at:
        #         from_date_str, to_date_str = created_at.split(" to ")
        #         from_date = datetime.strptime(from_date_str, "%d/%m/%y")
        #         to_date   = datetime.strptime(to_date_str, "%d/%m/%y")

        #         users = users.filter(created_at__range=[from_date, to_date])
        #     else:
        #         try:
        #             specific_date = datetime.strptime(created_at, '%d/%m/%y') 
        #             users = users.filter(created_at__date=specific_date) # Handle specific date
        #         except ValueError:
        #             pass # Handle invalid date format

        
        ## NOTE:- For Pagination
        custom_paginator = CustomPaginator(queryset, self.obj_per_page)
        paginated_data = custom_paginator.get_paginated_data(request)

        context = {
            'activitys': paginated_data['page_obj'],
            'page_obj': paginated_data['page_obj'],
            'page_range': paginated_data['page_range'],
            'queryset_count': queryset.count(),
        }

        return render(request, self.template_name, context)
    




"""
    ActivityLog Details
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')

class ActivityLogDetailsView(generic.DetailView, LoginRequiredMixin):
    model = ActivityLog
    template_name = "activitylog/data_view.html"
    context_object_name = "log_datas"

    def get_object(self, queryset=None):
        return get_object_or_404(ActivityLog.objects.all(), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        log_data = context['object']
        
        print("-----------------")
        print("Data =", log_data.data)
        print("-----------------")

        context['log_datas'] = log_data.data
        context['action_type'] = log_data.action_type
        return context

    

# class ActivityLogDetailsView(generic.DetailView, LoginRequiredMixin):
#     model = ActivityLog
#     template_name = "activitylog/data_view2.html"
#     context_object_name = "log_datas"

#     def get_object(self, queryset=None):
#         return get_object_or_404(ActivityLog.objects.all(), pk=self.kwargs['pk'])

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         log_data = context['object']
#         log_data.data = json.loads(log_data.data)  # Parse JSON string into dictionary

#         ## Oly Field Data
#         # fields_data = [item['fields'] for item in log_data.data]
        
#         print("-----------------")
#         print("Data =", log_data.data)
#         # print("Data =", fields_data)
#         # for item in log_data.data:
#             # print("Fields = ", item['fields'])
#             # print("Fields = ", item['fields']['email'])
#         print("-----------------")

#         # context['log_datas'] = [log_data]
#         context['log_datas'] = log_data.data
#         context['action_type'] = log_data.action_type
#         return context

        

    
# class ActivityLogDetailsView(generic.DetailView, LoginRequiredMixin):
#     model = ActivityLog
#     template_name = "activitylog/data_view.html"
#     context_object_name = "log_datas"

#     def get_context_data(self, *args, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['log_datas'] = self.model.objects.get(id=self.kwargs['pk'])
#         return data
