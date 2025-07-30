import json
import secrets
from urllib.parse import urlencode
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
)
from django.contrib.auth.models import User
from .models import UserProfile

LOGOUT_URL = 'https://alllogin.ku.ac.th/realms/KU-Alllogin/protocol/openid-connect/logout'
SERVER_METADATA_URL = 'https://alllogin.ku.ac.th/realms/KU-Alllogin/.well-known/openid-configuration'

oauth = OAuth()
oauth.register(
    'kusso',
    client_id=settings.KUSSO_CONFIG['client_id'],
    client_secret=settings.KUSSO_CONFIG['client_secret'],
    client_kwargs={
        'scope': 'openid basic',
        'token_endpoint_auth_method': 'client_secret_post',
    },
    server_metadata_url=SERVER_METADATA_URL,
    code_challenge_method='S256',
)


def login(request):
    client = oauth.create_client('kusso')
    redirect_path = reverse('kusso:authorize')
    redirect_uri = request.build_absolute_uri(redirect_path)
    code_verifier = secrets.token_urlsafe(64)
    request.session['next_url'] = request.GET.get('next', '')
    return client.authorize_redirect(
        request,
        redirect_uri,
        code_verifier=code_verifier,
        # code challenge is automatically created
    )


def logout(request):
    client = oauth.kusso

    if settings.LOGOUT_REDIRECT_URL:
        logout_redirect_url = settings.LOGOUT_REDIRECT_URL
    elif settings.LOGIN_REDIRECT_URL:
        logout_redirect_url = settings.LOGIN_REDIRECT_URL
    else:
        raise Exception(
            'Either LOGOUT_REDIRECT_URL or LOGIN_REDIRECT_URL must be set'
        )

    # It is possible the session authenticated by the old KUSSO still
    # remains, so certain session variables are not yet available.  In
    # that case, just logout of django and redirect to the login page.
    logout_params = {}
    try:
        logout_params['id_token_hint'] = request.session['kusso_id_token']
        kusso_logout_url = client.server_metadata['end_session_endpoint']
    except KeyError:
        django_logout(request)
        return redirect(logout_redirect_url)

    logout_params['post_logout_redirect_uri'] = (
        request.build_absolute_uri(logout_redirect_url)
    )

    django_logout(request)
    return redirect(kusso_logout_url + "?" + urlencode(logout_params))


def authorize(request):
    client = oauth.kusso
    token = client.authorize_access_token(
        request,
        scope='openid basic',
        # code verifier is automatically added
    )
    userinfo = token['userinfo']
    username = userinfo['uid']

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    # automatically create a user if CREATE_NONEXISTENT_USER is True
    if user is None and settings.KUSSO_CONFIG.get('create_new_user', False):
        user = User(username=username,
                    first_name=userinfo['givenname'],
                    last_name=userinfo['surname'])
        user.save()

    if user is None:
        messages.error(
            request,
            f"Username '{username}' does not exist.")
        return redirect('login')

    # record user profile and other auth-related info
    if hasattr(user, 'kusso_profile'):
        kusso_profile = user.kusso_profile
        kusso_profile.authenticated_at = timezone.now()
    else:
        kusso_profile = UserProfile(user=user,
                                    authenticated_at=timezone.now(),
                                    data=json.dumps(userinfo))
    kusso_profile.save()

    django_login(request,
                 user,
                 backend='django.contrib.auth.backends.ModelBackend')
    request.session['kusso_id_token'] = token.get('id_token')
    next_url = request.session.get('next_url') or settings.LOGIN_REDIRECT_URL

    return redirect(next_url)
