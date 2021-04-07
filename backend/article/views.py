from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, QueryDict
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response

from jsonschema import validate

from article.enum import Visibility
from article.models import Article

from utils.model_util import models_to_json,model_to_json
import json

class ArticleList(APIView):
    """ article list """
    permission_classes = (AllowAny,)

    def get(self, request):
        """ Retrieve all intend-for-publish articles from the database (restricted by user's visibility) """
        user = request.user
        if user.is_anonymous:
            articles = Article.objects.filter(visibility="ALL", published=True).values()
        else:
            articles = Article.objects.filter(visibility=user.role, published=True).values()

        response = {'articles': articles}
        # model to dict (and therefore model to json) does not work for date fields
        # so we get the queryset by calling values() and let DRF handles the serialization (Response)
        return Response(response)
