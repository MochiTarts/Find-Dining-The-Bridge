from django.conf import settings
# Module to upload files to the cloud
from google.oauth2 import service_account
from google.cloud import storage

import datetime
import string
import random


credentials = service_account.Credentials.from_service_account_info({
    "private_key": settings.GOOGLE_ANALYTICS_PRIVATE_KEY,
    "client_email": settings.GOOGLE_ANALYTICS_CLIENT_EMAIL,
    "token_uri": "https://oauth2.googleapis.com/token",
},
    scopes=['https://www.googleapis.com/auth/cloud-platform'],
)

client = storage.Client(project='scdining-winter2021', credentials=credentials)
DEV_BUCKET = 'dev-scdining'
TEST_BUCKET = 'test-scdining'
UAT_BUCKET = 'uat-scdining'
PRODUCTION_BUCKET = 'production-scdining'
API = 'https://storage.googleapis.com/'
IMAGE = 'image/png'
VIDEO = 'video/mp4'


def upload(file, content_type=None):
    """ Uploads a file to the bucket path. """
    bucket_path = DEV_BUCKET

    if settings.MAIN_SITE_URL is not None:
        if "test" in settings.MAIN_SITE_URL:
            bucket_path = TEST_BUCKET
        elif "uat" in settings.MAIN_SITE_URL:
            bucket_path = UAT_BUCKET
        else:
            bucket_path = PRODUCTION_BUCKET

    bucket = client.bucket(bucket_path)
    if content_type == VIDEO:
        name = generate_video_name()
    else:
        name = generate_name()
    blob = bucket.blob(name)
    blob.upload_from_file(file)
    return API + bucket_path + '/' + name


def generate_name():
    """ Generate a randomized filename
    for image files

    :return: the generated filename
    :rtype: str
    """
    letters = string.ascii_lowercase
    name = 'FILE-' + (''.join(random.choice(letters) for i in range(10))) + '-' + \
           str(datetime.datetime.now()) + '.png'
    return name


def generate_video_name():
    """ Generate a randomized filename
    for video files

    :return: the generated filename
    :rtype: str
    """
    letters = string.ascii_lowercase
    name = 'FILE-' + (''.join(random.choice(letters) for i in range(10))) + '-' + \
           str(datetime.datetime.now()) + '.mp4'
    return name


def delete(file_path):
    """ delete object from bucket if it is not a default

    :param file_path: the url to the file in google cloud bucket
    :type: str
    """

    if 'default-assets' in file_path:
        return
    if '/' == file_path:
        return
    elif API == file_path[:len(API)]:
        file_path = file_path.replace(API, '')
        bucket_path = file_path[:file_path.find('/')]
        bucket = client.bucket(bucket_path)
        bucket.delete_blob(file_path[file_path.find('/') + 1:])
    else:
        print('cannot parse invalid file')
