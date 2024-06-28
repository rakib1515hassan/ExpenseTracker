from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from django.urls import reverse


def is_superuser_or_staff(user):
    return user.is_superuser or user.is_staff



def is_superadmin(user):
    return user.is_superuser




def login_required_404(view_func):
    @method_decorator(login_required, name='dispatch')
    class RestrictedView(View):
        def get(self, request, *args, **kwargs):
            if not is_superuser_or_staff(request.user):
                raise Http404
            return view_func(request, *args, **kwargs)

    return RestrictedView.as_view()




class Custom404View(View):
    template_name = 'custom_404.html'

    def get(self, request, exception, *args, **kwargs):
        response = render(request, self.template_name, status=404)
        return response





""" NOTE: Alternatively Way
@method_decorator(user_passes_test(lambda user: user.is_superuser or user.is_staff), name='dispatch')



@method_decorator(user_passes_test(is_superuser_or_staff, 
    login_url=lambda: f"/admin/users/login/?next={reverse('user-details', args=[self.kwargs['pk']])}"), name='dispatch')


@method_decorator(user_passes_test(
        is_superuser_or_staff, 
        login_url='/admin/users/restrict/', 
        redirect_field_name='/admin/'), 
        name='dispatch'
    )
"""