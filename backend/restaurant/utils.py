from django.conf import settings
from django.core.mail import send_mail


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
