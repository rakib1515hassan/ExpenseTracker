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
from config.permission import is_superuser_or_staff, is_superadmin
from apps.core.utils2 import CustomPaginator, ExcelDataDownload
from apps.admin.forms import AdminCreationForm, AdminUpdateForm


"""
    Admin Create
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class AdminCreateView(generic.CreateView, LoginRequiredMixin):
    model = User
    form_class = AdminCreationForm
    template_name = "admin/create.html"
    success_url = reverse_lazy('admins:admin_list')

    def form_valid(self, form):
        admin_obj = form.save(commit=False)

        active    = self.request.POST.get('is_active', None)
        verified  = self.request.POST.get('is_verified', None)
        # admin     = self.request.POST.get('is_admin', None)
        superuser = self.request.POST.get('is_superuser', None)


        admin_obj.is_active = True if active == 'on' else False
        admin_obj.is_verified = True if verified == 'on' else False
        admin_obj.is_superuser = True if superuser == 'on' else False

        admin_obj.is_admin = True
        admin_obj.user_type = User.UserType.ADMIN
        admin_obj.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        field_errors = {field.name: field.errors for field in form}
        has_errors = any(field_errors.values())

        print("---------------------")
        print(f"Field = {field_errors}, HasErrors = {has_errors}")
        print(f"HasErrors = {has_errors}")
        print("---------------------")

        return self.render_to_response(self.get_context_data(
                form = form, 
                field_errors = field_errors, 
                has_errors   = has_errors
            ))
    



"""
    Admin List
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class AdminListView(View, LoginRequiredMixin):
    template_name = "admin/list.html"
    obj_per_page = 5

    def get_queryset(self):
        queryset = User.objects.filter(
                is_admin = True
            ).order_by('-created_at').exclude(id = self.request.user.id)

        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(id__icontains = search_query)  
                | Q(first_name__icontains = search_query)  
                | Q(last_name__icontains  = search_query)  
                | Q(email__icontains = search_query) 
                | Q(phone__icontains = search_query)
            )
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

        # ## NOTE:- Check if the export button is clicked
        # export_data = ''

        # if 'export' in request.GET:
        #     export_data = users
        
        # elif 'export_all' in request.GET:
        #     export_data = User.objects.all()

        # if export_data:

        #     # Prepare the data for Excel export
        #     excel_data = [
        #         ['No', 'Name', 'Email', 'Phone', 'User ID', 'User Type', 'Join Date', 'Verification Status'],
        #     ]

        #     for index, user in enumerate(export_data, start=1):
        #         excel_data.append([
        #             index,
        #             user.name,
        #             user.email,
        #             user.phone,
        #             str(user.id),
        #             # 'Customer' if user.user_type == 'customer' else 'Seller',
        #             user.user_type.capitalize(),
        #             # user.created_at.strftime('%d-%m-%Y %H:%M:%S'),
        #             user.created_at.strftime('%d-%m-%Y %I:%M:%S %p'),
        #             'Verified' if user.is_verified else 'Unverified',
        #         ])
            
        #     excel_exporter = ExcelDataDownload(excel_data, filename='UsersData_export')
        #     return excel_exporter.generate_response()


        ## NOTE:- For Pagination
        custom_paginator = CustomPaginator(queryset, self.obj_per_page)
        paginated_data = custom_paginator.get_paginated_data(request)

        context = {
            'admins': paginated_data['page_obj'],
            'page_obj': paginated_data['page_obj'],
            'page_range': paginated_data['page_range'],
            'queryset_count': queryset.count(),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        if 'delete_list' in request.POST:
            # Split the string into a list of IDs
            delete_ids = request.POST.get('delete_id_list', '').split(',')  

            # Convert the IDs to integers (This is not need because ID is uuid)
            # delete_ids = [int(id) for id in delete_ids if id.isdigit()]  

            # Delete the employee with the selected IDs
            User.objects.filter(id__in=delete_ids).delete()

        return redirect('admins:admin_list')




"""
    Admin Delete
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class AdminDeleteView(generic.DeleteView, LoginRequiredMixin):
    model = User
    success_url = reverse_lazy('admins:admin_list')

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id', None)
      
        if user_id is not None:
            try:
                user = User.objects.get(id = user_id)
                if user:
                    user.delete()
                    return redirect(self.success_url)
            except User.DoesNotExist:
                messages.error(request, "User Is Not Found!")
                messages.warning(request, "Please ensure the employee ID is correct,<br>then try to delete it.")
                return redirect('error_404')
            
            except ValidationError as e:
                messages.error(request, "Validation Error!")
                messages.warning(request, "Please ensure the employee ID is correct,<br>then try to delete it.")
                return redirect('error_404')
            
        messages.error(request, "Validation Error!")
        messages.warning(request, "ID Not Found!.")
        return redirect('error_404')
        
    # def delete(self, request, *args, **kwargs):
    #     try:
    #         user_id = self.kwargs['pk']  
    #         print("-------------------")
    #         print(f"Deleting user with ID: {user_id}")
    #         print("-------------------")
    #         return super().delete(request, *args, **kwargs)  # Let the parent class handle deletion
    #     except User.DoesNotExist:
    #         messages.error(request, "User Is Not Found!")
    #         return redirect('error_404')



"""
    Admin Details
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class AdminDetailsView(generic.DetailView, LoginRequiredMixin):
    model = User
    template_name = "admin/details.html"
    context_object_name = "admin"

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        data['admin'] = self.model.objects.get(id=self.kwargs['pk'])
        return data
    




"""
    Admin Update
"""
# @method_decorator(user_passes_test(is_superuser_or_staff, 
#     login_url=reverse_lazy('auth:login')), name='dispatch')
# class AdminUpdateView(generic.UpdateView, LoginRequiredMixin):
#     model = User
#     template_name = "admin/update.html"
#     form_class = AdminUpdateForm
#     context_object_name = "admin"

#     def get_success_url(self):
#         return reverse('admins:admin_details', kwargs={'pk': self.object.pk})
    
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         field_errors = {field.name: field.errors for field in form}
#         has_errors = any(field_errors.values())

#         print("---------------------")
#         print(f"Field = {field_errors}, HasErrors = {has_errors}")
#         print(f"HasErrors = {has_errors}")
#         print("---------------------")

#         return self.render_to_response(self.get_context_data(
#             form=form, 
#             field_errors=field_errors, 
#             has_errors=has_errors
#             ))
    



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class AdminUpdateView(generic.UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = User
    template_name = "admin/update.html"
    form_class = AdminUpdateForm
    context_object_name = "admin"
    permission_required = 'auth.change_user'  # Permission required to access this view

    def get_success_url(self):
        return reverse('admins:admin_details', kwargs={'pk': self.object.pk})
    
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

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            # raise PermissionDenied  ## If not return then use it alos
            return HttpResponseRedirect(
                reverse_lazy('admins:admin_details', kwargs={'pk': self.kwargs['pk']})
                )
        return super().dispatch(request, *args, **kwargs)




"""
    Permission Update
"""
@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class PermissionUpdateView(View):
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs['pk'])
            data = request.POST

            superadmin = str(data.get('is_superadmin'))
            admin = str(data.get('is_admin'))
            # user_type = data.get('user_type')
            active = data.get('is_active')
            verify = data.get('is_verified')

            # print("--------------------")
            # print("superadmin =", superadmin)
            # print("admin =", admin)
            # print("user_type =", user_type)
            # print("active =", active)
            # print("verify =", verify)
            # print("--------------------")

            if user:

                if superadmin == str(1) and admin == str(1):
                    user.is_superuser = True
                    user.is_admin = True
                    user.user_type = User.UserType.ADMIN

                elif superadmin == str(0) and admin == str(1):
                    user.is_superuser = False
                    user.is_admin = True
                    user.user_type = User.UserType.ADMIN

                elif superadmin == str(0) and admin == str(0):
                    user.is_superuser = False
                    user.is_admin = False
                    user.user_type = User.UserType.EMPLOYEE

                # if user_type:
                #     if user_type != user.user_type:
                #         user.user_type = user_type

                if (active and verify):
                    if active != user.is_active:
                        user.is_active = active
                    if verify != user.is_verified:
                        user.is_verified = verify

                user.save()
                response_data = {'success': True}
                return JsonResponse(response_data)

        except User.DoesNotExist:
            response_data = {'success': False}
            return JsonResponse(response_data)
        


