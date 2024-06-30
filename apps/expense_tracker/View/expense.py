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
    Expense Create
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class ExpenseCreateView(LoginRequiredMixin, generic.CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "expense/create.html"
    success_url = reverse_lazy('expense_tracker:expense_list')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user  ## Pass the user to the form
    #     return kwargs
    
    def form_valid(self, form):
        expense_obj = form.save(commit=False)
        expense_obj.owner = self.request.user
        
        # Check if total expenses exceed the budget
        budget = Budget.objects.filter(owner=self.request.user, category=expense_obj.category).first()
        if budget:
            if budget.total_expenses() + expense_obj.amount > budget.amount:
                messages.error(
                    self.request,
                    f"Error: Adding this expense exceeds the budget for category '{budget.category.name}'!"
                )
                return self.form_invalid(form)
        
        expense_obj.save()
        messages.success(self.request, "Expense created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        field_errors = {field.name: field.errors for field in form}
        has_errors = any(field_errors.values())

        # print("---------------------")
        # print(f"Field Errors: {field_errors}")
        # print(f"Has Errors: {has_errors}")
        # print("---------------------")

        return self.render_to_response(
            self.get_context_data(
                form=form,
                field_errors=field_errors,
                has_errors=has_errors
            )
        )
    

"""
    Expense List
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class ExpenseListView(View, LoginRequiredMixin):
    template_name = "expense/list.html"
    obj_per_page  = 10

    def get_queryset(self):
        queryset = Expense.objects.filter(owner=self.request.user)
        search_query = self.request.GET.get('search', '')
        category_id  = self.request.GET.get('category_id', '')
        joining_from = self.request.GET.get('joining_from', '')
        joining_to   = self.request.GET.get('joining_to', '')

        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query)
            )

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if joining_from:
            queryset = queryset.filter(created_at__gte=joining_from)

        if joining_to:
            queryset = queryset.filter(created_at__lte=joining_to)

        return queryset


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # ## NOTE:- Check if the export button is clicked
        export_data = ''

        if 'export' in request.GET:
            export_data = queryset
        
        elif 'export_all' in request.GET:
            export_data = Expense.objects.filter(owner = request.user)

        if export_data:

            # Prepare the data for Excel export
            excel_data = [
                ['No', 'Categotry Name', 'Budget Amount', 'Expense Amount', 'Description', 'Create At', 'Updated At'],
            ]

            for index, expences in enumerate(export_data, start=1):

                excel_data.append([
                    index,
                    expences.category.name,
                    expences.category.budget.amount,
                    expences.amount,
                    expences.description,

                    expences.created_at.strftime('%d-%m-%Y %I:%M:%S %p'),
                    expences.updated_at.strftime('%d-%m-%Y %I:%M:%S %p'),
                ])

            
            excel_exporter = ExcelDataDownload(excel_data, filename='Expences_export')
            return excel_exporter.generate_response()

        ## NOTE:- For Pagination
        custom_paginator = CustomPaginator(queryset, self.obj_per_page)
        paginated_data = custom_paginator.get_paginated_data(request)

        categories = Category.objects.filter(owner=request.user)
        context = {
            'expenses': paginated_data['page_obj'],
            'page_obj': paginated_data['page_obj'],
            'page_range': paginated_data['page_range'],
            'queryset_count': queryset.count(),
            'categories': categories,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'delete_list' in request.POST:
            # Split the string into a list of IDs
            delete_ids = request.POST.get('delete_id_list', '').split(',')  
            Expense.objects.filter(id__in=delete_ids).delete()
        return redirect('expense_tracker:expense_list')
    



"""
    Expense Update
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class ExpenseUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Expense
    template_name = "expense/update.html"
    form_class = ExpenseForm
    context_object_name = "expense"
    success_url = reverse_lazy('expense_tracker:expense_list')

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['user'] = self.request.user  ## Pass the current user to the form
    #     return kwargs

    def form_valid(self, form):
        expense_obj = form.save(commit=False)

        ## Get the original amount of the expense being updated
        original_expense = Expense.objects.get(pk=self.object.pk)
        original_amount = original_expense.amount

        ## Check if total expenses exceed the budget
        budget = Budget.objects.filter(owner=self.request.user, category=expense_obj.category).first()
        if budget:
            ## Calculate the total expenses excluding the original amount of the expense being updated
            new_total_expense = budget.total_expenses() - original_amount + expense_obj.amount
            if new_total_expense > budget.amount:
                messages.error(
                    self.request,
                    f"Error: Updating this expense exceeds the budget for category '{budget.category.name}'!"
                )
                return self.form_invalid(form)

        expense_obj.save()
        messages.success(self.request, "Expense updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        field_errors = {field.name: field.errors for field in form}
        has_errors = any(field_errors.values())

        # print("---------------------")
        # print(f"Field = {field_errors}, HasErrors = {has_errors}")
        # print(f"HasErrors = {has_errors}")
        # print("---------------------")

        return self.render_to_response(self.get_context_data(
            form=form, 
            field_errors=field_errors, 
            has_errors=has_errors
            ))
    



"""
    Expense Delete
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class ExpenseDeleteView(generic.DeleteView, LoginRequiredMixin):
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
    
