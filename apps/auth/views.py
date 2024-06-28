from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sessions.models import Session
from django.contrib import messages

from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils import timezone

from django.db.models import Q, Count, F
from django.db.models.functions import ExtractMonth, ExtractYear

from django.http import HttpRequest, HttpResponse, JsonResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage

from datetime import datetime, timedelta
from random import randint
from django.conf import settings

from django.views import View
from django.views import generic

## Custom 
from config.permission import is_superuser_or_staff, is_superadmin



# Create your views here.
class LoginView(View):
    template_name = "auth/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, request.get_host()):
                return redirect(next_url)
            return redirect('dashboards:home')
        
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me') == 'on'  # Check if "Remember Me" checkbox is checked

        if User.objects.filter(email=email).first():
            auth_user = authenticate(request, email=email, password=password)

            if auth_user is not None:
                if auth_user.is_admin:
                    login(request, auth_user)

                    # Set session expiry based on "Remember Me" checkbox
                    if remember_me:
                        # Set session expiry to settings.REMEMBER_ME_EXPIRY seconds
                        request.session.set_expiry(settings.REMEMBER_ME_EXPIRY)
                    else:
                        # Set session expiry to default (settings.SESSION_COOKIE_AGE)
                        request.session.set_expiry(0)  # Expire session when the browser is closed

                    next_url = request.GET.get('next')

                    if next_url and url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                        return redirect(next_url)
                    return redirect('dashboards:home')
                
                else:
                    error = 'Only admin users can login.'
                    return render(request, self.template_name, {'error': error})

            else:
                response = {
                    'error': 'Invalid password',
                    'error_type': 'Password',
                    'email': email,
                    'password': password,
                }
                return render(request, self.template_name, response)

        else:
            response = {
                'error': 'Invalid email',
                'error_type': 'Email',
                'email': email,
                'password': password,
            }
            return render(request, self.template_name, response)




@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, "auth/logout.html")
    



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class ChangePasswordView(LoginRequiredMixin, View):
    template_name = "auth/change_password.html"
    success_url = reverse_lazy('auth:password-change')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user = request.user  # Update the user's password and keep them logged in

        if not authenticate(email=user.email, password=old_password):
            messages.error(request, "Old password is incorrect.")
            return render(request, self.template_name)

        if password and password2 and password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, self.template_name)

        if password and len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, self.template_name)

        user.set_password(password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Congrats! Password successfully changed.")
        return redirect(self.success_url)