from django.conf import settings
from django.contrib.auth import get_user_model

from subscriber_profile.models import SubscriberProfile
from restaurant_owner.models import RestaurantOwner
from newsletter.models import NLUser

from google.oauth2 import service_account
from googleapiclient.discovery import build

from datetime import date

import os


credentials = service_account.Credentials.from_service_account_info({
    "client_email": settings.GOOGLE_OAUTH2_CLIENT_EMAIL,
    "token_uri": "https://oauth2.googleapis.com/token",
    "private_key": settings.GOOGLE_OAUTH2_PRIVATE_KEY,
},
    scopes=['https://www.googleapis.com/auth/spreadsheets'],
    subject="info@finddining.ca")

spreadsheet_id = os.environ.get('SPREADSHEET_ID')

User = get_user_model()


def create_user_emails_sheets_subscribers():
    """ Create a google spreadsheets of all subscribers that are signed up to receive newsletters

    Returns:
        Void, creates google sheets under info@finddining.ca
    """
    input_range = "Sheet1"

    sheetsService = build(
        'sheets', 'v4', credentials=credentials, cache_discovery=False)

    # Empty sheet
    sheetsService.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=input_range).execute()

    # Get all basic users' email
    users = list(User.objects.filter(is_active=True,
                                     role="BU").values('email', 'profile_id'))

    # Check their consent status and update accordingly
    subscribers = []
    for user in users:
        if user['profile_id'] != None:
            profile = SubscriberProfile.objects.get(id=user['profile_id'])
            status = profile.consent_status
            if status == "IMPLIED" and profile.expired_at < date.today():
                profile.consent_status = "EXPIRED"
                profile.save()
            elif status == "EXPRESSED" or status == "IMPLIED":
                user.pop('profile_id')
                user.update({"first_name": profile.first_name,
                             "last_name": profile.last_name, "consent_status": profile.consent_status})
                subscribers.append(user)

    # Get newsletter only users' email
    nlusers = list(NLUser.objects.all())

    # Check their consent status and update accordingly
    for nluser in nlusers:
        status = nluser.consent_status
        if status == "IMPLIED" and nluser.expired_at < date.today():
            nluser.consent_status = "EXPIRED"
            nluser.save()
        elif status == "EXPRESSED" or status == "IMPLIED":
            subscribers.append({"email": nluser.email, "first_name": nluser.first_name,
                                "last_name": nluser.last_name, "consent_status": nluser.consent_status})

    print(subscribers)
    # Append user info into values (only users that has email verified)
    values = [['Email', 'First name', 'Last name', 'Consent Status']]
    for subscriber in subscribers:
        values.append(list(subscriber.values()))

    body = {
        'values': values
    }

    try:
        sheetsService.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=input_range,
                                                     valueInputOption="USER_ENTERED", body=body).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
        raise error
        # return None

    # Automatically format the sheets
    requests = [
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": 0,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 4
                }
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 4
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(textFormat)"
            }
        }
    ]

    body = {
        'requests': requests
    }

    try:
        sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
        raise error


def create_user_emails_sheets_restaurant_owners():
    """ Create a google spreadsheets of all restaurant owners that are signed up to receive newsletters

    Returns:
        Void, creates google sheets under info@finddining.ca
    """
    input_range = "Sheet1"

    sheetsService = build(
        'sheets', 'v4', credentials=credentials, cache_discovery=False)

    # Empty sheet
    sheetsService.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=input_range).execute()

    # Get all basic users' email
    restaurant_owners = list(User.objects.filter(
        is_active=True, role="RO").values('email', 'username'))

    # Append user info into values (only users that has email verified)
    values = [['Email', 'Username']]
    for restaurant_owner in restaurant_owners:
        values.append(list(restaurant_owner.values()))

    body = {
        'values': values
    }

    try:
        sheetsService.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=input_range,
                                                     valueInputOption="USER_ENTERED", body=body).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
        raise error
        # return None

    # Automatically format the sheets
    requests = [
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": 0,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 2
                }
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(textFormat)"
            }
        }
    ]

    body = {
        'requests': requests
    }

    try:
        sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
        raise error


def create_user_emails_sheets_all():
    """ Create a google spreadsheets of all users that are signed up to receive newsletters

    Returns:
        Void, creates google sheets under info@finddining.ca
    """
    input_range = "Sheet1"

    sheetsService = build(
        'sheets', 'v4', credentials=credentials, cache_discovery=False)

    # Empty sheet
    sheetsService.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=input_range).execute()

    # Get all basic users' email
    users = list(User.objects.filter(is_active=True,
                                     role="BU").values('email', 'username', 'role', 'profile_id'))

    # Check their consent status and update accordingly
    subscribers = []
    for user in users:
        if user['profile_id'] != None:
            profile = SubscriberProfile.objects.get(id=user['profile_id'])
            status = profile.consent_status
            if status == "IMPLIED" and profile.expired_at < date.today():
                profile.consent_status = "EXPIRED"
                profile.save()
            elif status == "EXPRESSED" or status == "IMPLIED":
                user.pop('profile_id')
                subscribers.append(user)
    # Get newsletter only users' email
    nlusers = list(NLUser.objects.all())

    # Check their consent status and update accordingly
    for nluser in nlusers:
        status = nluser.consent_status
        if status == "IMPLIED" and nluser.expired_at < date.today():
            nluser.consent_status = "EXPIRED"
            nluser.save()
        elif status == "EXPRESSED" or status == "IMPLIED":
            subscribers.append({"email": nluser.email, "username": nluser.first_name,
                                "role": "NL"})

    # Get all basic users' email
    restaurant_owners = list(
        User.objects.filter(is_active=True, role="RO").values('email', 'username', 'role'))

    # Append user info into values (only users that has email verified)
    values = [['Email', 'Username', 'Role']]
    for subscriber in subscribers:
        values.append(list(subscriber.values()))
    for restaurant_owner in restaurant_owners:
        values.append(list(restaurant_owner.values()))

    body = {
        'values': values
    }

    try:
        sheetsService.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=input_range,
                                                     valueInputOption="USER_ENTERED", body=body).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
        raise error
        # return None

    # Automatically format the sheets
    requests = [
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": 0,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": 3
                }
            }
        },
        {
            "repeatCell": {
                "range": {
                    "sheetId": 0,
                    "startRowIndex": 0,
                    "endRowIndex": 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": 3
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat(textFormat)"
            }
        }
    ]

    body = {
        'requests': requests
    }

    try:
        sheetsService.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
        raise error
