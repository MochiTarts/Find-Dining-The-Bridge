from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()

def send_posts_notify_email(post, restaurant_name, request):
    """ Send email to all admins, notifying
    them of a new restaurant post. Email will contain the link
    to the RestaurantPost change_form page on Django admin site.

    :param post: the newly created post by a restaurant owner
    :type post: :class: `RestaurantPost`
    :param restaurant_name: the name of the restaurant that made this post
    :type restaurant_name: str
    :param request: the request to inserting a new post
    :type request: HttpRequest object
    """
    subject = "New Restaurant Post on Find Dining"
    admins = list(User.objects.filter(
        is_superuser=True).values_list('email', flat=True))

    link = get_current_site(request).domain
    if link == "localhost:8000":
        link = "http://" + link + "/api/admin/restaurant/restaurantpost/" + \
            str(post._id) + "/change/"
    else:
        link = "https://" + link + "/api/admin/restaurant/restaurantpost/" + \
            str(post._id) + "/change/"
            
    content = "<p>New restaurant post posted by: {}</p>".format(restaurant_name) + \
              "<a href={}>Link to post</a>".format(link)
    send_mail(subject, strip_tags(content), from_email="admin@finddining.ca",
        recipient_list=admins, html_message=content)
              

def send_approval_email(names, receiver, profile_title, profile_type):
    """ Sends an email to the restaurant owner, informing them
    that their restaurant or dish is now approved and
    is viewable to all users on the Find Dining site

    :param names: restaurant owner name(s)
    :type names: list of str
    :param receiver: restaurant owner's email
    :type receiver: str
    :param profile_title: name of the restaurant of dish
    :type profile_title: str
    :param profile_type: tells whether the admin approved of a
        restaurant or a dish (must be either 'restaurant' or 'food')
    :type profile_type: str
    """
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
    content += '<p>Your Find Dining team</p>'

    if profile_type == 'restaurant':
        subject = "Restaurant Profile Approved by Find Dining"
    else:
        subject = "Food Profile Approved by Find Dining"

    send_mail(subject, strip_tags(content), from_email="admin@finddining.ca",
              recipient_list=[receiver], html_message=content)


def send_reject_email(names, receiver, profile_title, profile_type):
    """ Sends an email to the restaurant owner, informing them
    that their restaurant or dish is has been rejected by
    an admin

    :param names: restaurant owner name(s)
    :type names: list of str
    :param receiver: restaurant owner's email
    :type receiver: str
    :param profile_title: name of the restaurant of dish
    :type profile_title: str
    :param profile_type: tells whether the admin rejected a
        restaurant or a dish (must be either 'restaurant' or 'food')
    :type profile_type: str
    """
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
    content += '<p>Your Find Dining team</p>'

    if profile_type == 'restaurant':
        subject = "Restaurant Profile Rejected by Find Dining"

    else:
        subject = "Food Profile Rejected by Find Dining"

    send_mail(subject, strip_tags(content), from_email="admin@finddining.ca",
              recipient_list=[receiver], html_message=content)


def send_unpublish_email(names, receiver, profile_title, profile_type):
    """ Sends an email to the restaurant owner, informing them
    that their restaurant or dish is has been unpublished from
    the live site by an admin

    :param names: restaurant owner name(s)
    :type names: list of str
    :param receiver: restaurant owner's email
    :type receiver: str
    :param profile_title: name of the restaurant of dish
    :type profile_title: str
    :param profile_type: tells whether the admin unpublished a
        restaurant or a dish (must be either 'restaurant' or 'food')
    :type profile_type: str
    """
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
    content += '<p>Your Find Dining team</p>'

    message = ""
    if profile_type == 'restaurant':
        subject = "Restaurant Profile Unpublished by Find Dining"

    else:
        subject = "Food Profile Unpublished by Find Dining"

    send_mail(subject, strip_tags(content), from_email="admin@finddining.ca",
              recipient_list=[receiver], html_message=content)
