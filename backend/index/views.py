from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags

from drf_yasg.utils import swagger_auto_schema
from index import swagger


class EmailView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=swagger.SendEmail, responses=swagger.send_email_post_response,
                         operation_id="POST /email/send/")
    def post(self, request):
        data = request.data
        try:
            subject = data['subject']
            content = data['content']
            send_mail(subject, strip_tags(content), from_email="info@finddining.ca",
                      recipient_list=["info@finddining.ca"], html_message=content)
            return JsonResponse({'message': 'email has been sent'})
        except Exception:
            return JsonResponse({'message': 'unable to send email', 'code': 'send_email_failed'}, status=429)


def angularLogIn(request, path=''):
    """
    redirect to angular login page
    """
    return redirect(settings.VIEW_REDIRECT_URL + '/login')
