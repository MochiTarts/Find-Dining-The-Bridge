import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings

credentials = service_account.Credentials.from_service_account_info({
    "client_email": settings.GOOGLE_OAUTH2_CLIENT_EMAIL,
    "token_uri": "https://oauth2.googleapis.com/token",
    "private_key": settings.GOOGLE_OAUTH2_PRIVATE_KEY,
},
    scopes=['https://www.googleapis.com/auth/spreadsheets'],
    subject="info@finddining.ca")

sheetsService = build(
    'sheets', 'v4', credentials=credentials, cache_discovery=False)
spreadsheet_id = "1xkY8ORsca41mJsIbxBhbsZUJ-3hDRetlbpns3ATFU1k"


def create_user_emails_sheets():
    """ Create a google spreadsheets of all users that are signed up to receive newsletters

    Returns:
        Void, creates google sheets under info@finddining.ca
    """
    input_range = "Sheet1"

    # Empty sheet
    sheetsService.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=input_range).execute()

    #verified = get_all_verified_email_from_SDUser()
    #verified = get_all_verified_email_from_firebase()

    # Get all users' first name, last name, consent status, expired at, and email
    # SDUsers = list(SDUser.objects.all().values('firstname', 'lastname', 'email', 'consent_status', 'expired_at'))
    # newsletter_users = list(NLUser.objects.all().values('first_name', 'last_name', 'email', 'consent_status', 'subscribed_at', 'expired_at'))

    # Append user info into values (only users that has email verified)
    values = [['First name', 'Last name', 'Email', 'Consent Status']]
    # for sduser in SDUsers:
    #     if sduser.get('consent_status') == "EXPRESSED" or sduser.get("expired_at") != None and sduser.get("consent_status") == "IMPLIED" and sduser.get("expired_at") > date.today():
    #         sduser.pop('expired_at')
    #         if sduser.get('email').lower() in verified:
    #             values.append(list(sduser.values()))
    #     elif sduser.get("expired_at") != None and sduser.get("consent_status") == "IMPLIED" and sduser.get("expired_at") <= date.today():
    #         SDUser.objects.filter(email=sduser.get('email')).update(consent_status="EXPIRED")

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


create_user_emails_sheets()
