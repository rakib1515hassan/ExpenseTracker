from django.shortcuts import render, redirect
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

## Custom 
from apps.core.Utils.utils import CustomPaginator, ExcelDataDownload
from config.permission import is_superuser_or_staff, is_superadmin
from apps.expense_tracker.models import Category, Budget, Expense
from apps.expense_tracker.forms import ExpenseForm



"""
    Expenses vs. Budget
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class ExpensesvsBudgetListView(View, LoginRequiredMixin):
    template_name = "expense_vs_budget/list.html"
    obj_per_page  = 10

    def get_queryset(self):
        queryset = Category.objects.filter(owner=self.request.user)
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                
            )
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        ## NOTE:- For Pagination
        custom_paginator = CustomPaginator(queryset, self.obj_per_page)
        paginated_data = custom_paginator.get_paginated_data(request)

        categories = Category.objects.filter(owner=request.user)
        context = {
            'categories': paginated_data['page_obj'],
            'page_obj': paginated_data['page_obj'],
            'page_range': paginated_data['page_range'],
            'queryset_count': queryset.count(),
        }

        return render(request, self.template_name, context)

    




    


    model = Expense
    success_url = reverse_lazy('expense_tracker:expense_list')

    def post(self, request, *args, **kwargs):
        expense_id = request.POST.get('expense_id', None)
      
        if expense_id is not None:
            try:
                expense = Expense.objects.get(id = expense_id)
                if expense:
                    expense.delete()
                    return redirect(self.success_url)
            except Expense.DoesNotExist:
                messages.error(request, "Expense Is Not Found!")
                messages.warning(request, "Please ensure the Expense ID is correct,<br>then try to delete it.")
                return redirect('error_404')
            
            except ValidationError as e:
                messages.error(request, "Validation Error!")
                messages.warning(request, "Please ensure the Expense ID is correct,<br>then try to delete it.")
                return redirect('error_404')
            
        messages.error(request, "Validation Error!")
        messages.warning(request, "ID Not Found!.")
        return redirect('error_404')