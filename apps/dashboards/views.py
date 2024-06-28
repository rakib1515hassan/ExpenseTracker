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

from django.views import View
from django.views import generic

## Custom 
from config.permission import is_superuser_or_staff, is_superadmin





@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=reverse_lazy('auth:login')), name='dispatch')
class Home(generic.TemplateView):
    template_name = "dashboards/dashboard.html"

    def get(self, request, *args, **kwargs):

        # context = {
            
        # }

        return render(request, self.template_name)