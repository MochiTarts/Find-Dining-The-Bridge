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
        """ Retrieve all articles from the database (depending on user visibility) """
        user = request.user
        if user.is_anonymous:
            articles = Article.objects.filter(visibility="ALL").values()
        else:
            articles = Article.objects.filter(visibility=user.role).values()

        response = {'articles': articles}
        return Response(response)
