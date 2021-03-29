from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from datetime import date

credentials = service_account.Credentials.from_service_account_info({
    "client_email": settings.GOOGLE_ANALYTICS_CLIENT_EMAIL,
    "token_uri": "https://oauth2.googleapis.com/token",
    "private_key": settings.GOOGLE_ANALYTICS_PRIVATE_KEY,
},
    scopes=['https://www.googleapis.com/auth/analytics.readonly'],
)

analyticService = build('analytics', 'v3', credentials=credentials, cache_discovery=False)


def get_access_token():
    """ Function for retrieving OAuth2 access token """

    return credentials.get_access_token().access_token


def get_analytics_data(restaurant_id):
    """
    Function to retrieve view data given page view
    :param: restaurant_id: id of the restaurant whose page views will be retrieved
    :return: Google Analytics Core Reporting response data given the specific query
             parameters
    """

    VIEW_ID = settings.GA_VIEW_ID

    accounts = analyticService.management().accounts().list().execute()
    
    first_day_of_month = date.today().replace(day=1)

    return analyticService.data().ga().get(
        ids='ga:' + VIEW_ID,
        start_date=str(first_day_of_month),
        end_date='today',
        metrics='ga:pageviews',
        filters='ga:pagePath==/restaurant?restaurantId='+restaurant_id,
        dimensions='ga:date',
        prettyPrint=True).execute()

#print(get_analytics_data('60305a70ad235a859cfe8731'))