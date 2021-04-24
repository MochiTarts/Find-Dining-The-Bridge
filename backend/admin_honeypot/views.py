import django
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic

from admin_honeypot.forms import HoneypotLoginForm
from admin_honeypot.models import HoneypotLoginAttempt
from admin_honeypot.signals import honeypot
from login_audit.models import get_client_ip_address, get_client_user_agent

class AdminHoneypot(generic.FormView):
    template_name = 'admin_honeypot/login.html'
    form_class = HoneypotLoginForm

    def dispatch(self, request, *args, **kwargs):
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
        path = self.request.get_full_path()
        context.update({
            'app_path': path,
            REDIRECT_FIELD_NAME: reverse('admin_honeypot:index'),
            'title': _('Log in'),
        })
        return context

    def form_valid(self, form):
        return self.form_invalid(form)

    def form_invalid(self, form):
        '''
        instance = HoneypotLoginAttempt.objects.create(
            username=self.request.POST.get('username'),
            session_key=self.request.session.session_key,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT'),
            path=self.request.get_full_path(),
        )
        '''
        instance = HoneypotLoginAttempt.objects.create(
            username=self.request.POST.get('username'),
            session_key=self.request.session.session_key,
            ip_address=get_client_ip_address(self.request),
            user_agent=get_client_user_agent(self.request),
            path=self.request.get_full_path(),
        )
        honeypot.send(sender=HoneypotLoginAttempt,
                      instance=instance, request=self.request)
        return super(AdminHoneypot, self).form_invalid(form)


@receiver(honeypot)
def notify_admin_for_melicious_login_attempt(sender, **kwargs):
    # username, ip_address, session_key, user_agent, timestamp, path
    # print(sender.username)
    pass
