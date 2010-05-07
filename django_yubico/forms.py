import re

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

RE_PUBLIC_ID = re.compile(r'^[cbdefghijklnrtuv]{12}$')
RE_TOKEN = re.compile(r'^[cbdefghijklnrtuv]{32,64}$')

class LoginForm(forms.Form):
	username = forms.CharField(label = _('Username'))
	otp = forms.RegexField(label = _('OTP'), widget = forms.PasswordInput(attrs = {'style': 'background:url("/site_media/images/yubiright_16x16.gif") no-repeat scroll 2px 2px white; padding-left:20px;'}), \
						regex = RE_TOKEN, min_length = 34, max_length = 64)
		
	def clean(self):
		self.user = None
		username = self.cleaned_data.get('username')
		otp = self.cleaned_data.get('otp')
		
		if username and otp:
			self.user = authenticate(username = username, otp = otp)
		
			if self.user is None:
				raise forms.ValidationError(_('The provided OTP is invalid.'))

		return self.cleaned_data
	
class PasswordForm(forms.Form):
	password = forms.CharField(label = _('Password'), widget = forms.PasswordInput(), \
							required = True)
	
	def __init__(self, *args, **kwargs):
		self.user = kwargs['user']
		del(kwargs['user'])
		super(PasswordForm, self).__init__(*args, **kwargs)
		
	def clean_password(self):
		password = self.cleaned_data['password']
		
		if not self.user.check_password(password):
			raise forms.ValidationError(_('The provided password is incorrect'))