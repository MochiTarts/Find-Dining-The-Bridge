from django.conf import settings
from django.core.mail import mail_admins
from django.template.loader import render_to_string
from django.urls import reverse

from admin_honeypot.signals import honeypot
from sduser.utils import get_domain_and_protocal

def notify_admins(instance, request, **kwargs):
    domain, protocal = get_domain_and_protocal(request, None, None)
    path = reverse('admin:admin_honeypot_honeypotloginattempt_change',
                   args=(instance.pk,))
    #domain = request.get_host()
    admin_detail_url = '{0}://{1}{2}'.format(protocal, domain, path)
    context = {
        'request': request,
        'instance': instance,
        'admin_detail_url': admin_detail_url,
    }
    subject = render_to_string(
        'admin_honeypot/email_subject.html', context).strip()
    message = render_to_string(
        'admin_honeypot/email_message.html', context).strip()
    mail_admins(subject=subject, message=message)


if getattr(settings, 'ADMIN_HONEYPOT_EMAIL_ADMINS', True):
    honeypot.connect(notify_admins)
