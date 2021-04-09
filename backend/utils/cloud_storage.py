# Module to upload files to the cloud
from google.oauth2 import service_account
from google.cloud import storage
import datetime
import string
import random
from django.conf import settings

credentials = service_account.Credentials.from_service_account_info({
    "private_key": settings.GOOGLE_ANALYTICS_PRIVATE_KEY,
    "client_email": settings.GOOGLE_ANALYTICS_CLIENT_EMAIL,
    "token_uri": "https://oauth2.googleapis.com/token",
},
    scopes=['https://www.googleapis.com/auth/cloud-platform'],
)

client = storage.Client(project='scdining-winter2021', credentials=credentials)
DEV_BUCKET = 'dev-scdining'
PRODUCTION_BUCKET = 'production-scdining'
API = 'https://storage.googleapis.com/'
IMAGE = 'image/png'
VIDEO = 'video/mp4'


def upload(file, bucket_path, content_type=None):
    """ Uploads a file to the bucket path. """
    #if settings.ENVIRONMENT == 'prod':
    #    bucket_path = PRODUCTION_BUCKET  # Use production bucket if in production mode
    bucket = client.bucket(bucket_path)
    if content_type == VIDEO:
        name = generate_video_name()
    else:
        name = generate_name()
    blob = bucket.blob(name)
    blob.upload_from_file(file)
    return API + bucket_path + '/' + name


def generate_name():
    """Generate a randomized filename"""
    letters = string.ascii_lowercase
    name = 'FILE-' + (''.join(random.choice(letters) for i in range(10))) + '-' + \
           str(datetime.datetime.now()) + '.png'
    return name

def generate_video_name():
    """Generate a randomized filename"""
    letters = string.ascii_lowercase
    name = 'FILE-' + (''.join(random.choice(letters) for i in range(10))) + '-' + \
           str(datetime.datetime.now()) + '.mp4'
    return name


def delete(file_path):
    """
    delete object from bucket if it is not a default
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