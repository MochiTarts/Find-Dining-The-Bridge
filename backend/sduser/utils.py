from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from sduser.tokens import sduser_activation_token_generator

UserModel = get_user_model()

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and not user.is_blocked and sduser_activation_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(
            request,
            template_name='verify_email/success.html',
            context={
                'msg': 'Thank you for confirming your email with Find Dining. Your account has been activated. Please click the button below to login.',
                'status': 'Verification Successful!',
                'link': reverse('login')
            }
        )
    else:
        return render(
            request,
            template_name='verify_email/failure.html',
            context={
                'msg': 'Activation link has been used or is invalid!',
                'status': 'Verification Failed!',
            }
        )

def send_email_verification(user, request=None, site=None):
    if site is not None:
        domain = site
    else:
        domain = get_current_site(request).domain
    subject = 'Verify Your Email for Find Dining'
    email_template_name = 'verify_email/verification.html'
    message = render_to_string(email_template_name, {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': sduser_activation_token_generator.make_token(user),
            })
    send_mail(subject, strip_tags(message), from_email='noreply<noreply@gmail.com>',
                        recipient_list=[user.email], html_message=message, fail_silently=False)


def send_email_deactivate(user, request=None, site=None):
    if site is not None:
        domain = site
    else:
        domain = get_current_site(request).domain
    subject = 'Account Deactivation for Find Dining'
    email_template_name = 'verify_email/deactivation.html'
    message = render_to_string(email_template_name, {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': sduser_activation_token_generator.make_token(user),
            })
    send_mail(subject, strip_tags(message), from_email='noreply<noreply@gmail.com>',
                        recipient_list=[user.email], html_message=message, fail_silently=False)


def send_email_deactivate_notify(user, request=None, site=None):
    if site is not None:
        domain = site
    else:
        domain = get_current_site(request).domain
    subject = 'Account Deactivation for Find Dining'
    email_template_name = 'verify_email/deactivation_notify.html'
    message = render_to_string(email_template_name, {
                'user': user,
                'domain': domain,
            })
    send_mail(subject, strip_tags(message), from_email='noreply<noreply@gmail.com>',
                        recipient_list=[user.email], html_message=message, fail_silently=False)



def send_email_password_reset(user, request=None, site=None):
    if site is not None:
        domain = site
    else:
        domain = get_current_site(request).domain
    
    subject = "Password Reset on Find Dining"
    email_template_name = 'registration/password_reset_email_user.html'

    message = render_to_string(email_template_name, {
    "email":user.email,
    'site_name': 'Find Dining',
    'protocol': 'https',
    'domain': domain,
    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    'user': user,
    'token': default_token_generator.make_token(user),
    })
    send_mail(subject, strip_tags(message), from_email='noreply<noreply@gmail.com>',
                        recipient_list=[user.email], html_message=message, fail_silently=False)