from django.utils import timezone
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, QueryDict
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework.permissions import AllowAny

from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response

from jsonschema import validate

from article.enum import Visibility
from article.models import Article
from article import swagger

from utils.model_util import models_to_json,model_to_json
import json

from drf_yasg.utils import swagger_auto_schema

class ArticleList(APIView):
    """ article list """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses=swagger.article_all_response,
        operation_id="GET /article/all/")
    def get(self, request):
        """ Retrieve all intend-for-publish articles from the database (restricted by user's visibility) """
        user = request.user
        if user.is_anonymous:
            articles = Article.objects.filter(visibility="ALL", published=True).values()
        else:
            articles = Article.objects.filter(visibility__in=[user.role, "ALL"], published=True).values()

        response = {'articles': articles}
        # model to dict (and therefore model to json) does not work for date fields
        # so we get the queryset by calling values() and let DRF handles the serialization (Response)
        return Response(response)

class ArticleView(APIView):
    """ article view """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(responses=swagger.article_id_response,
        operation_id="GET /article/{id}/")
    def get(self, request, id):
        """ Retrieve an article given id (restricted by user's visibility) """
        user = request.user

        if user.is_anonymous:
            article = Article.objects.filter(visibility="ALL", published=True, id=id).values()
        else:
            article = Article.objects.filter(visibility__in=[user.role, "ALL"], published=True, id=id).values()
        # evaluate it instead of calling exists() because we need the cached result in response
        if article:
            response = {'article': article[0]}
        else:
            raise NotFound('Cannot find article with id: ' + str(id))
        # model to dict (and therefore model to json) does not work for date fields
        # so we get the queryset by calling values() and let DRF handles the serialization (Response)
        return Response(response)
