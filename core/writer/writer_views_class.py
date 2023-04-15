import core
from core import utils_path, config
from core.writer.writer_class import WriterClass


class WriterViewsClass(WriterClass):
    """Class for writing a django Views class on python file,

               create a python class file named views.py


               Attributes:
                    name: Name of app
                    client_id: client_id for authentication with OAuth2
                    client_secret: client_secret for authentication with OAuth2
                    """

    def __init__(self, name: str, client_id: str, client_secret: str, **kwargs):
        super().__init__('views', utils_path.path_views(name), name, **kwargs)
        self.extends = 'viewsets.ModelViewSet'
        self.client_id = client_id
        self.client_secret = client_secret

    def write(self):
        self.content = f"""from django.contrib.auth import login
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.views import APIView
import requests
from custom_apps.{self.name}.permissions import {self.name.capitalize()}Permission
from custom_apps.{self.name}.serializers import {self.name.capitalize()}Serializer
from custom_apps.{self.name}.models import {self.name.capitalize()}
from user.models import CustomUser


class {self.name.capitalize()}ViewSet(viewsets.ModelViewSet):
    queryset = {self.name.capitalize()}.objects.all()
    serializer_class = {self.name.capitalize()}Serializer 
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [{self.name.capitalize()}Permission]
    
    
class GoogleLogin(APIView):
    REDIRECT_URI = '{config.base_url}/api/{self.name}/callback/'
    CLIENT_ID = '{self.client_id}'
    CLIENT_SECRET = '{self.client_secret}'
    SCOPES = {config.SCOPES}
    
    def get(self, request):
        session = requests.Session()
        flow = session.prepare_request(
            requests.Request(
                method='GET',
                url='https://accounts.google.com/o/oauth2/v2/auth',
                {self._create_param()}
            )
        )
        return redirect(flow.url)
        
        
class GoogleCallback(APIView):
    REDIRECT_URI = '{config.base_url}/api/{self.name}/callback/'
    CLIENT_ID = '{self.client_id}'
    CLIENT_SECRET = '{self.client_secret}'
    
    def get(self, request):
        code = request.GET.get('code')
        session = requests.Session()
        token_url = 'https://oauth2.googleapis.com/token'
        {self._create_token_param()}
        
        token_response = session.post(token_url, data=token_params)
        token_data = token_response.json()
        access_token = token_data['access_token']

        if not access_token:
            return HttpResponseBadRequest('Token missing')

        request.session['access_token'] = access_token

        email = verify_google_token(access_token)

        if not email:
            return HttpResponseBadRequest('Invalid token')

        try:
            user = CustomUser.objects.get(email=email)
            app_roles = user.app_role.split(', ')
            if 'user_{self.name}' not in app_roles:
                user.app_role = user.app_role + ', ' + 'user_{self.name}'
                user.save()
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_user(email=email, app='{self.name}', app_role='user_{self.name}')

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        
        return redirect('/api/{self.name}/')
        
        
{self._verify_google_token()}
"""
        self.print()

    def _create_token_param(self):
        return """token_params = {
            'code': code,
                'client_id': self.CLIENT_ID,
                'client_secret': self.CLIENT_SECRET,
                'redirect_uri': self.REDIRECT_URI,
                'grant_type': 'authorization_code',
            }"""

    def _create_param(self):
        return """params={
                        'client_id': self.CLIENT_ID,
                        'redirect_uri': self.REDIRECT_URI,
                        'scope': ' '.join(['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']),
                        'response_type': 'code',
                        'access_type': 'offline',
                        'prompt': 'consent'
                    }"""

    def _verify_google_token(self):
        return """def verify_google_token(token: str):
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    userinfo_response = requests.get(userinfo_url, headers={'Authorization': f'Bearer {token}'})
    userinfo_data = userinfo_response.json()
    return userinfo_data['email']"""


