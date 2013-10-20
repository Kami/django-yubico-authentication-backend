from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from django.views.decorators.cache import never_cache

from forms import LoginForm, PasswordForm

# Ask for the user password after the token
YUBIKEY_USE_PASSWORD = getattr(settings, 'YUBICO_USE_PASSWORD', True)

# Name of the session key which stores user id
YUBIKEY_SESSION_USER_ID = getattr(settings, 'YUBICO_SESSION_USER_ID',
                                  'yubicodjango_user_id')

# Name of the session key which stores the name of the backend user used to log
# in.
YUBIKEY_SESSION_AUTH_BACKEND = getattr(settings, 'YUBICO_SESSION_AUTH_BACKEND',
                                       'yubicodjango_auth_backend')

# Name of the session key which stores attempt counter
YUBIKEY_SESSION_ATTEMPT_COUNTER = getattr(settings,
                                          'YUBIKEY_SESSION_ATTEMPT_COUNTER',
                                          'yubicodjango_counter')

# Name of the session key which stores number of password attemps
YUBIKEY_PASSWORD_ATTEMPTS = getattr(settings, 'YUBICO_PASSWORD_ATTEMPTS', 3)

# Django Yubico session keys
SESSION_KEYS = [YUBIKEY_SESSION_USER_ID, YUBIKEY_SESSION_AUTH_BACKEND,
                YUBIKEY_SESSION_ATTEMPT_COUNTER]


@never_cache
def login(request, template_name='django_yubico/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name,
                                      settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.user

            if YUBIKEY_USE_PASSWORD:
                # Dual factor authentication is enabled, user still needs to
                # enter his password
                request.session[YUBIKEY_SESSION_USER_ID] = user.pk
                request.session[YUBIKEY_SESSION_AUTH_BACKEND] = user.backend
                request.session[YUBIKEY_SESSION_ATTEMPT_COUNTER] = 1

                return HttpResponseRedirect(reverse('yubico_django_password'))
            else:
                auth_login(request=request, user=user)
                return HttpResponseRedirect(redirect_to)
    else:
        form = LoginForm()

    dictionary = {'form': form, redirect_field_name: redirect_to}
    return render_to_response(template_name, dictionary,
                              context_instance=RequestContext(request))


@never_cache
def password(request, template_name='django_yubico/password.html',
             redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the password form and handles the login action.
    """

    redirect_to = request.REQUEST.get(redirect_field_name,
                                      settings.LOGIN_REDIRECT_URL)

    for key in SESSION_KEYS:
        # Make sure all the required session keys are present
        value = request.session.get(key, None)

        if value is None:
            return HttpResponseRedirect(reverse('yubico_django_login'))

    user_id = request.session[YUBIKEY_SESSION_USER_ID]
    auth_backend = request.session[YUBIKEY_SESSION_AUTH_BACKEND]

    user = User.objects.get(pk=user_id)
    user.backend = auth_backend

    if request.method == 'POST':
        form = PasswordForm(request.POST, user=user)

        if form.is_valid():
            auth_login(request=request, user=user)
            reset_user_session(session=request.session)
            return HttpResponseRedirect(redirect_to)
        else:
            # Limit the number of password attempts per token
            request.session[YUBIKEY_SESSION_ATTEMPT_COUNTER] += 1

            if request.session[YUBIKEY_SESSION_ATTEMPT_COUNTER] > \
               YUBIKEY_PASSWORD_ATTEMPTS:
                # Maximum number of attemps has been reached. Require user to
                # start from scratch.
                reset_user_session(session=request.session)
                return HttpResponseRedirect(reverse('yubico_django_login'))
    else:
        form = PasswordForm(user=user)

    dictionary = {'form': form, redirect_field_name: redirect_to}
    return render_to_response(template_name, dictionary,
                              context_instance=RequestContext(request))


def reset_user_session(session):
    """
    Remove all the Django Yubico related keys from the provided session.
    """
    for key in SESSION_KEYS:
        try:
            del session[key]
        except KeyError:
            pass
