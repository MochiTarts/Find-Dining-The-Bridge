from django.contrib.auth import get_user_model
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

from subscriber_profile.models import SubscriberProfile
from restaurant.models import PendingRestaurant, Restaurant
from utils.math import calculate_distance

from operator import itemgetter
import ast

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
    message = render_to_string('verify_email/verification.html', {
                'user': user,
                'domain': domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': sduser_activation_token_generator.make_token(user),
            })
    send_mail(subject, strip_tags(message), from_email='noreply<noreply@gmail.com>',
                        recipient_list=[user.email], html_message=message)


def get_nearby_restaurants(user_id, role):
    """ Retrieves the 5 nearest approved restaurants
    in proximity to the GEO_location of the sduser given
    the user_id and their role

    :param user_id: the id of the sduser
    :type user_id: int
    :param role: the sduser's role (BU or RO)
    :type role: str
    :return: list of dict objects, each one containing the restaurant's id
            and distance from the sduser, in ascending order
    :rtype: list of dict
    """
    user = None
    if role == 'BU':
        user = SubscriberProfile.objects.filter(
            user_id=user_id).first()
    else:
        user = PendingRestaurant.objects.filter(
            owner_user_id=user_id).first()

    if not user:
        raise ObjectDoesNotExist("The user with the given user_id: "+ user_id +" does not exist")

    user_location = ast.literal_eval(user.GEO_location)
    nearest = []
    restaurants = list(Restaurant.objects.all())
    for restaurant in restaurants:
        if role == 'RO' and restaurant._id == user._id:
            continue
        user_location = ast.literal_eval(restaurant.GEO_location)
        distance = calculate_distance(user_location, user_location)
        nearest.append(
            {"restaurant": str(restaurant._id), "distance": distance})

    nearest = sorted(nearest, key=itemgetter("distance"))
    if (len(nearest) > 5):
        nearest = nearest[:5]
    return nearest