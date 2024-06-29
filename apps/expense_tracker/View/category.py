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
from apps.expense_tracker.models import Category
from apps.expense_tracker.forms import CategoryForm


"""
    Category Create
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "category/create.html"
    success_url = reverse_lazy('expense_tracker:category_list')

    def form_valid(self, form):
        category_obj = form.save(commit=False)
        category_obj.owner = self.request.user
        category_obj.save()
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
    Category List
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class CategoryListView(View, LoginRequiredMixin):
    template_name = "category/list.html"
    obj_per_page  = 2

    def get_queryset(self):
        queryset = Category.objects.filter(owner = self.request.user)
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
            'categories': paginated_data['page_obj'],
            'page_obj': paginated_data['page_obj'],
            'page_range': paginated_data['page_range'],
            'queryset_count': queryset.count(),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'delete_list' in request.POST:
            # Split the string into a list of IDs
            delete_ids = request.POST.get('delete_id_list', '').split(',')  
            Category.objects.filter(id__in=delete_ids).delete()
        return redirect('expense_tracker:category_list')
    



"""
    Category Update
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class CategoryUpdateView(generic.UpdateView, LoginRequiredMixin):
    model = Category
    template_name = "category/update.html"
    form_class = CategoryForm
    context_object_name = "category"
    success_url = reverse_lazy('expense_tracker:category_list')
    
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
    Category Delete
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class CategoryDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = Category
    success_url = reverse_lazy('expense_tracker:category_list')

    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id', None)
      
        if category_id is not None:
            try:
                category = Category.objects.get(id = category_id)
                if category:
                    category.delete()
                    return redirect(self.success_url)
            except Category.DoesNotExist:
                messages.error(request, "Category Is Not Found!")
                messages.warning(request, "Please ensure the Category ID is correct,<br>then try to delete it.")
                return redirect('error_404')
            
            except ValidationError as e:
                messages.error(request, "Validation Error!")
                messages.warning(request, "Please ensure the Category ID is correct,<br>then try to delete it.")
                return redirect('error_404')
            
        messages.error(request, "Validation Error!")
        messages.warning(request, "ID Not Found!.")
        return redirect('error_404')