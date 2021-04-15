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


def get_access_token():
    """ Function for retrieving OAuth2 access token """

    return credentials.get_access_token().access_token


def get_analytics_data(restaurant_id, format_type):
    """
    Function to retrieve view data given page view
    :param: restaurant_id: id of the restaurant whose page views will be retrieved
    :return: Google Analytics Core Reporting response data given the specific query
        parameters
    """
    analyticService = build(
        'analytics', 'v3', credentials=credentials, cache_discovery=False)

    VIEW_ID = settings.GA_VIEW_ID
    start_date = ''
    end_date = ''
    dimensions = ''
    if format_type == 'daily':
        start_date = str(date.today().replace(day=1))
        end_date = 'today'
        dimensions = 'ga:date'
    elif format_type == 'hourly':
        start_date = '2daysAgo'
        end_date = '2daysAgo'
        dimensions = 'ga:hour'
    elif format_type == 'alltime':
        start_date = '2021-05-01'
        end_date = 'today'
        dimensions = 'ga:month'

    data = analyticService.data().ga().get(
        ids='ga:' + VIEW_ID,
        start_date=start_date,
        end_date=end_date,
        metrics='ga:pageviews',
        filters='ga:pagePath==/restaurant?restaurantId='+restaurant_id,
        dimensions=dimensions,
        prettyPrint=True,
        fields='totalsForAllResults,rows').execute()
    return data

# print(get_analytics_data('605b55d192c9e40e98c1877a'))
