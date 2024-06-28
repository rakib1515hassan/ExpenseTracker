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
from apps.expense_tracker.models import Budget
from apps.expense_tracker.forms import BudgetForm


"""
    Admin Create
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class BudgetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "budget/create.html"
    success_url = reverse_lazy('expense_tracker:budget_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  ## Pass the user to the form
        return kwargs

    def form_valid(self, form):
        budget_obj = form.save(commit=False)
        budget_obj.owner = self.request.user
        budget_obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        field_errors = {field.name: field.errors for field in form}
        has_errors = any(field_errors.values())

        print("---------------------")
        print(f"Field Errors: {field_errors}")
        print(f"Has Errors: {has_errors}")
        print("---------------------")

        return self.render_to_response(
            self.get_context_data(
                form=form,
                field_errors=field_errors,
                has_errors=has_errors
            )
        )
    

"""
    Admin List
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class BudgetListView(View, LoginRequiredMixin):
    template_name = "budget/list.html"
    obj_per_page  = 10

    def get_queryset(self):
        queryset = Budget.objects.filter(owner = self.request.user)
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains = search_query)  
                | Q(name__icontains = search_query)  
            )
        return queryset


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        ## NOTE:- For Pagination
        custom_paginator = CustomPaginator(queryset, self.obj_per_page)
        paginated_data = custom_paginator.get_paginated_data(request)

        context = {
            'budgets': paginated_data['page_obj'],
            'page_obj': paginated_data['page_obj'],
            'page_range': paginated_data['page_range'],
            'queryset_count': queryset.count(),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'delete_list' in request.POST:
            # Split the string into a list of IDs
            delete_ids = request.POST.get('delete_id_list', '').split(',')  
            Budget.objects.filter(id__in=delete_ids).delete()
        return redirect('expense_tracker:budget_list')
    



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class BudgetUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Budget
    template_name = "budget/update.html"
    form_class = BudgetForm
    context_object_name = "budget"
    success_url = reverse_lazy('expense_tracker:budget_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  ## Pass the current user to the form
        return kwargs

    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        field_errors = {field.name: field.errors for field in form}
        has_errors = any(field_errors.values())

        print("---------------------")
        print(f"Field = {field_errors}, HasErrors = {has_errors}")
        print(f"HasErrors = {has_errors}")
        print("---------------------")

        return self.render_to_response(self.get_context_data(
            form=form, 
            field_errors=field_errors, 
            has_errors=has_errors
            ))
    



"""
    Admin Delete
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class BudgetDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = Budget
    success_url = reverse_lazy('expense_tracker:budget_list')

    def post(self, request, *args, **kwargs):
        budget_id = request.POST.get('budget_id', None)
      
        if budget_id is not None:
            try:
                budget = Budget.objects.get(id = budget_id)
                if budget:
                    budget.delete()
                    return redirect(self.success_url)
            except Budget.DoesNotExist:
                messages.error(request, "Budget Is Not Found!")
                messages.warning(request, "Please ensure the Budget ID is correct,<br>then try to delete it.")
                return redirect('error_404')
            
            except ValidationError as e:
                messages.error(request, "Validation Error!")
                messages.warning(request, "Please ensure the Budget ID is correct,<br>then try to delete it.")
                return redirect('error_404')
            
        messages.error(request, "Validation Error!")
        messages.warning(request, "ID Not Found!.")
        return redirect('error_404')