import re

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

RE_PUBLIC_ID = re.compile(r'^[cbdefghijklnrtuv]{12}$')
RE_TOKEN = re.compile(r'^[cbdefghijklnrtuv]{32,64}$')

# Multi mode (default = False)
YUBICO_MULTI_MODE = getattr(settings, 'YUBICO_MULTI_MODE', False)

# How many OTPs user needs to enter when multi mode is enabled
YUBICO_MULTI_NUMBER = getattr(settings, 'YUBICO_MULTI_NUMBER', 3)

STYLE = ''''background:url("/site_media/images/yubiright_16x16.gif") no-repeat
scroll 2px 2px white; padding-left:20px;'''
PASSWORD_INPUT_WIDGET_ATTRS = {'style': STYLE}


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

        min_length = 34
        max_length = 64

        if not YUBICO_MULTI_MODE:
            widget = forms.PasswordInput(attrs=PASSWORD_INPUT_WIDGET_ATTRS)
            self.fields['otp'] = forms.RegexField(label=_('OTP'),
                                                  widget=widget,
                                                  regex=RE_TOKEN,
                                                  min_length=min_length,
                                                  max_length=max_length)
        else:
            for index in range(0, YUBICO_MULTI_NUMBER):
                label = _('OTP %d' % (index + 1))
                widget = forms.PasswordInput(attrs=PASSWORD_INPUT_WIDGET_ATTRS)

                field = forms.RegexField(label=label, widget=widget,
                                         regex=RE_TOKEN,
                                         min_length=min_length,
                                         max_length=max_length)
                self.fields['otp_%d' % index] = field

    def clean(self):
        username = self.cleaned_data.get('username')

        otp_list = []
        if not YUBICO_MULTI_MODE:
            otp = self.cleaned_data.get('otp')
            otp_list.append(otp)
        else:
            for index in range(0, YUBICO_MULTI_NUMBER):
                otp = self.cleaned_data.get('otp_%d' % index)
                otp_list.append(otp)

        if username and otp_list:
            self.user = authenticate(username=username, otp=otp_list)

        if self.user is None:
            raise forms.ValidationError(_('The provided OTP is invalid.'))

        return self.cleaned_data


class PasswordForm(forms.Form):
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(),
                               required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        del(kwargs['user'])
        super(PasswordForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data['password']

        if not self.user.check_password(password):
            msg = _('The provided password is incorrect')
            raise forms.ValidationError(msg)
