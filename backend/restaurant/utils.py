from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from restaurant.models import RestaurantPost

User = get_user_model()

def send_posts_notify_email(post, restaurant_name):
    """ Send email to all admins, notifying
    them of a new restaurant post

    :param post: the newly created post by a restaurant owner
    :type post: :class: `RestaurantPost`
    :param restaurant_name: the name of the restaurant that made this post
    :type restaurant_name: str
    """
    subject = "New Restaurant Post on Find Dining"
    admins = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))

    #link = settings.SITE_URL + "/api/admin/restaurant/restaurantpost/" + \
    #        str(post._id) + "/change/"

    link = "http://localhost:8000" + "/api/admin/restaurant/restaurantpost/" + \
            str(post._id) + "/change/"
            
    content = "<p>New restaurant post posted by: {}</p>".format(restaurant_name) + \
              "<a href={}>Link to post</a>".format(link)
    
    send_mail(subject, strip_tags(content), from_email="admin@finddining.ca",
              recipient_list=admins, html_message=content)
              

def send_approval_email(names, receiver, profile_title, profile_type):
    # if names list is empty
    if not names:
        names = ["Restaurant Owner"]
    content = '<p>Hello ' + ', '.join(names) + ',</p>'
    if profile_type == 'restaurant':
        content += '<p>Your restaurant profile for <i>' + profile_title + \
            '</i> has been approved and is published to the live site.</p>'
    else:
        content += '<p>Your food profile for <i>' + profile_title + \
            '</i> has been approved and is published to the live site.</p>'
    content += '<p>Thanks,</p>'
    content += '<p>Your SCDining team</p>'

    if profile_type == 'restaurant':
        subject = "Restaurant Profile Approved by Find Dining"
    else:
        subject = "Food Profile Approved by Find Dining"

    send_mail(subject, strip_tags(content), from_email="admin@finddining.ca",
              recipient_list=[receiver], html_message=content)


def send_reject_email(names, receiver, profile_title, profile_type):
    # if names list is empty
    if not names:
        names = ["Restaurant Owner"]
    content = '<p>Hello ' + ', '.join(names) + ',</p>'
    if profile_type == 'restaurant':
        content += '<p>Your restaurant profile for <i>' + profile_title + \
            '</i> has been rejected and the changes will not be applied to the live site.</p>'
    else:
        content += '<p>Your food profile for <i>' + profile_title + \
            '</i> has been rejected and the changes will not be applied to the live site.</p>'
    content += '<p>Please review the comments from administrator and make appropriate changes.</p>'
    if profile_type == 'restaurant':
        content += '<p>Once you feel confident about your restaurant profile, feel free to submit it again for us to reivew!</p>'
    else:
        content += '<p>Once you feel confident about your food profile, feel free to submit it again for us to reivew!</p>'
    content += '<p>Thanks,</p>'
    content += '<p>Your SCDining team</p>'

    if profile_type == 'restaurant':
        subject = "Restaurant Profile Rejected by Find Dining"

    else:
        subject = "Food Profile Rejected by Find Dining"

    send_mail(subject, strip_tags(content), from_email="admin@finddining.ca",
              recipient_list=[receiver], html_message=content)


def send_unpublish_email(names, receiver, profile_title, profile_type):
    # if names list is empty
    if not names:
        names = ["Restaurant Owner"]
    content = '<p>Hello ' + ', '.join(names) + ',</p>'
    if profile_type == 'restaurant':
        content += '<p>Your restaurant profile for <i>' + profile_title + \
            '</i> has been unpublished from the live site.</p>'
    else:
        content += '<p>Your food profile for <i>' + profile_title + \
            '</i> has been unpublished from the live site.</p>'
    content += '<p>Please check the comments from administrator for the detail reason.</p>'
    content += '<p>Note: this does not apply to the newest submission that has not been reviewed yet. If you have submitted a newer profile please wait for it to be reviewed.</p>'
    content += '<p>Thanks,</p>'
    content += '<p>Your SCDining team</p>'

    message = ""
    if profile_type == 'restaurant':
        subject = "Restaurant Profile Unpublished by Find Dining"

    else:
        subject = "Food Profile Unpublished by Find Dining"

    send_mail(subject, strip_tags(content), from_email="admin@finddining.ca",
              recipient_list=[receiver], html_message=content)
