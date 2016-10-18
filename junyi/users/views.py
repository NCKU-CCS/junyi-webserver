import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from .models import UserProfile

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

class FBUserLogin(APIView):

    def get(self, request):
        request_url = "https://www.facebook.com/v2.8/dialog/oauth?\
            client_id=%s&redirect_uri=%s&scope=%s" % \
            (settings.FB_CLIENT_ID, settings.FB_REDIRECT_URI, \
             ','.join(settings.FB_SCOPE))
        return redirect(request_url)

class FBUserRedirect(APIView):

    def get(self, request):
        code = request.GET.get('code', '')
        request_url = "https://graph.facebook.com/v2.8/oauth/access_token?\
            client_id=%s&redirect_uri=%s&client_secret=%s&code=%s" % \
            (settings.FB_CLIENT_ID, settings.FB_REDIRECT_URI, \
             settings.FB_SECRET_KEY, code)
        req = requests.get(request_url)
        access_token = req.json().get('access_token', '')

        # Get User Data
        request_url = "https://graph.facebook.com/me?\
            fields=id,name,age_range,link,gender,locale,\
            timezone,updated_time,verified,picture,email\
            &access_token=%s" % (access_token)
        req = requests.get(request_url)
        fb_user_dict = req.json()

        # Get User or Create User or Update User
        user_filter = User.objects.filter(username=fb_user_dict['email'])
        if len(user_filter) > 0:
            user = User.objects.get(username=fb_user_dict['email'])
            userprofile = UserProfile.objects.get(user=user)
        else:
            user = User(username=fb_user_dict['email'],
                        password=User.objects.make_random_password(),
                        email=fb_user_dict['email'])
            user.save()
            userprofile = UserProfile(user=user)

        userprofile.email=fb_user_dict['email'],
        userprofile.fb_id=fb_user_dict['id']
        userprofile.name=fb_user_dict['name']
        userprofile.link=fb_user_dict['link']
        userprofile.gender=fb_user_dict['gender']
        userprofile.locale=fb_user_dict['locale']
        userprofile.timezone=fb_user_dict['timezone']
        userprofile.picture_url=fb_user_dict['picture']['data']['url']
        userprofile.access_token=access_token
        userprofile.save()

        login(request, user)

        return Response(status=status.HTTP_200_OK)

