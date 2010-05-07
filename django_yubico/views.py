from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.template import loader, RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse

from django.views.decorators.cache import never_cache

from forms import LoginForm, PasswordForm

# Ask for the user password after the token
YUBIKEY_USE_PASSWORD = getattr(settings, 'YUBICO_USE_PASSWORD', True)

# Session key name
YUBIKEY_SESSION_USER = getattr(settings, 'YUBICO_SESSION_USER', 'yubicodjango_user')

# Session key name for password attempts
YUBIKEY_ATTEMPT_COUNTER = getattr(settings, 'YUBIKEY_ATTEMPT_COUNTER', 'yubicodjango_counter')

# Session key name for password attempts
YUBIKEY_PASSWORD_ATTEMPTS = getattr(settings, 'YUBICO_PASSWORD_ATTEMPTS', 3)

@never_cache
def login(request,
		template_name = 'django_yubico/login.html',
		redirect_field_name = REDIRECT_FIELD_NAME):
	"""Displays the login form and handles the login action."""

	redirect_to = request.REQUEST.get(redirect_field_name, '')

	if request.method == 'POST':
		form = LoginForm(request.POST)
		
		if form.is_valid():
			user = form.user
			
			if YUBIKEY_USE_PASSWORD:
				# Two way authentication is enabled, user still needs to enter
				# his password
				request.session[YUBIKEY_SESSION_USER] = user
				request.session[YUBIKEY_ATTEMPT_COUNTER] = 1
				
				return HttpResponseRedirect(reverse('yubico_django_password'))
			else:
				auth_login(request, user)

				return HttpResponseRedirect(redirect_to or settings.LOGIN_REDIRECT_URL)
	else:
		form = LoginForm()

	return render_to_response(template_name, {'form': form, redirect_field_name: redirect_to}, \
							context_instance = RequestContext(request))
	
@never_cache
def password(request,
		template_name = 'django_yubico/password.html',
		redirect_field_name = REDIRECT_FIELD_NAME):
	"""Displays the password form and handles the login action."""
	
	redirect_to = request.REQUEST.get(redirect_field_name, '')
	
	if not request.session.get(YUBIKEY_SESSION_USER) or not request.session.get(YUBIKEY_ATTEMPT_COUNTER):
		return HttpResponseRedirect(reverse('yubico_django_login'))
	
	if request.method == 'POST':
		form = PasswordForm(request.POST, user = request.session[YUBIKEY_SESSION_USER])
		
		if form.is_valid():
			auth_login(request, request.session[YUBIKEY_SESSION_USER])
			
			try:
				del(request.session[YUBIKEY_SESSION_USER])
			except KeyError:
				pass
			
			try:
				del(request.session[YUBIKEY_ATTEMPT_COUNTER])
			except KeyError:
				pass
			
			return HttpResponseRedirect(redirect_to or settings.LOGIN_REDIRECT_URL)
		else:
			# Limit the number of password attempts per token
			request.session[YUBIKEY_ATTEMPT_COUNTER] += 1
			
			if request.session[YUBIKEY_ATTEMPT_COUNTER] > YUBIKEY_PASSWORD_ATTEMPTS:
				del(request.session[YUBIKEY_SESSION_USER])
				del(request.session[YUBIKEY_ATTEMPT_COUNTER])
				return HttpResponseRedirect(reverse('yubico_django_login'))
	else:
		form = PasswordForm(user = request.session[YUBIKEY_SESSION_USER])
		
	return render_to_response(template_name, {'form': form, redirect_field_name: redirect_to}, \
							context_instance = RequestContext(request))