import logging
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth import login,logout
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from .models import UserProfile
from .task import *

logger = logging.getLogger(__name__)


class Register(ListCreateAPIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/register.html'

    def get(self, request):

        serializer = UserRegistrationSerializer
        logger.info("Customer registration page")
        return Response({'serializer': serializer})

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            send_registration_mail(request.data)
            logger.info("Customer successfully registered")
            return JsonResponse({'msg': 'data created', 'response': serializer.data}, status=201)

        else:
            return JsonResponse({'msg': 'data not created'}, status=409)


class ValidateUsername(APIView):

    def post(self, request):
        db_username = UserProfile.objects.filter(username=request.data['username']).first()
        if db_username:
            return Response({'msg': 'Username is already taken! Please try another!'}, status=404)
        else:
            return Response({'msg': 'Good to go! This username is available.'})


class ValidateEmail(APIView):

    def post(self, request):
        db_email = UserProfile.objects.filter(email=request.data['email']).first()

        if db_email:
            return Response({'msg': 'Email already there! Try another one..!'}, status=404)
        else:
            return Response({'msg': 'Good to go! You can use this email.'})


class LoginView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/login.html'

    def get(self, request):
        serializer = UserLoginSerializer
        logger.info("Customer login page")
        return Response({'serializer': serializer})

    def post(self, request, format=None):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        db_username = UserProfile.objects.filter(username=username).first()
        if db_username is not None:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logger.info("login successfull")
                    return JsonResponse({'msg': 'login successfull'}, status=200)
                else:
                    return Response({'msg': 'user is not active'}, status=400)
            else:
                return JsonResponse({'msg': 'Invalid Credentials'}, status=401)
        else:
            return JsonResponse({'msg': 'Invalid Credentials'}, status=401)


class AccountPage(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        logger.info("Customer account page")
        return Response(template_name="customer/accountpage.html")

    def put(self, request, *args, **kwargs):
        update_data = request.data
        user_data = UserProfile.objects.get(email=update_data['email_id'])
        serializer = UserRegistrationSerializer(user_data, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info("Account page updated")
        return JsonResponse({'msg': 'Data Updated!!'}, status=200)


class DeleteUserAccount(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]

    def delete(self, request):
        data = request.data
        UserProfile.objects.filter(email=data).delete()
        logger.info("Customer account deleted")
        return JsonResponse({'msg': 'Account Deleted'}, status=203)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'customer/login.html'

    def get(self, request):
        logout(request)
        logger.info("Logged out!")
        return HttpResponseRedirect('/rest-auth/loginview/')


