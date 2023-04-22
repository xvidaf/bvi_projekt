from admin_honeypot.forms import HoneypotLoginForm
from admin_honeypot.models import LoginAttempt
from admin_honeypot.signals import honeypot

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic

from web_honeypot.models import HoneypotSetting
from web_honeypot.utils import log_previous_page


class AdminHoneypot(generic.FormView):
    template_name = 'admin_honeypot/login.html'
    form_class = HoneypotLoginForm

    def dispatch(self, request, *args, **kwargs):

        log_previous_page(request)

        if not request.path.endswith('/'):
            return redirect(request.path + '/', permanent=True)

        # Django redirects the user to an explicit login view with
        # a next parameter, so emulate that.
        login_url = reverse('admin_honeypot:login')
        if request.path != login_url:
            return redirect_to_login(request.get_full_path(), login_url)

        return super(AdminHoneypot, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=form_class):
        return form_class(self.request, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(AdminHoneypot, self).get_context_data(**kwargs)
        context.update({
            **AdminSite().each_context(self.request),
            'app_path': self.request.get_full_path(),
            REDIRECT_FIELD_NAME: reverse('admin_honeypot:index'),
            'title': _('Log in'),
        })
        return context

    def form_valid(self, form):
        return self.form_invalid(form)

    def form_invalid(self, form):
        if HoneypotSetting.objects.first().log_previous_page is True:
            user_ip = self.request.META.get('HTTP_X_FORWARDED_FOR')
            if user_ip:
                ip_address = user_ip.split(',')[0]
            else:
                ip_address = self.request.META.get('REMOTE_ADDR')
            #ip_address, is_routable = get_client_ip(self.request)
            instance = LoginAttempt.objects.create(
                username=self.request.POST.get('username'),
                password=self.request.POST.get('password'),
                session_key=self.request.session.session_key,
                ip_address=ip_address.split(':')[0],
                user_agent=self.request.META.get('HTTP_USER_AGENT'),
                path=self.request.get_full_path(),
            )
            honeypot.send(sender=LoginAttempt, instance=instance, request=self.request)
        return super(AdminHoneypot, self).form_invalid(form)
