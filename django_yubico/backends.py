from yubico.yubico import Yubico
from yubico.yubico_exceptions import YubicoError

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, check_password

from models import YubicoKey

# How much time can pass between the time when the first and last OTP is generated
YUBICO_MULTI_TIMEOUT = getattr(settings, 'YUBICO_MULTI_TIMEOUT', 10)

class YubicoBackend:
	"""
	This backend requires a valid username and OTP from user to login.
	"""
	def authenticate(self, username = None, otp = None):
		if not otp:
			return None

		count = len(otp)
		device_id = otp[0][:12]

		try:
			yubico = YubicoKey.objects.get(user__username = username, \
									device_id = device_id)
		except YubicoKey.DoesNotExist:
			return None
		
		if not yubico.user.is_active or not yubico.enabled:
			return None
		
		secret_key = yubico.secret_key or None
		client = Yubico(yubico.client_id, secret_key)
		
		try:
			if count > 1:
				# More then 1 OTP provided, using multi mode
				status = client.verify_multi(otp_list = otp, max_time_window = YUBICO_MULTI_TIMEOUT)
			else:
				status = client.verify(otp[0])
		except YubicoError:
			return None
		
		if not status:
			return None
		
		return yubico.user
	
	def get_user(self, user_id):
		try:
			return User.objects.get(pk = user_id)
		except User.DoesNotExist:
			return None
		
class YubicoBackendStaff(ModelBackend):
	"""
	If this backend is enabled, normal users can login with just a password
	but staff and super users are required to enter a valid OTP to log in.
	"""
	def authenticate(self, *args, **kwargs):
		user = super(YubicoBackendStaff, self).authenticate(*args, **kwargs)
		
		if user and (user.is_staff or user.is_superuser):
			return None
		else:
			return user
		
class YubicoBackendRequireYubikey(ModelBackend):
	"""
	If this backend is enabled, each user with at least one active YubiKey
	must enter a valid OTP to log in.
	"""
	def authenticate(self, *args, **kwargs):
		user = super(YubicoBackendRequireYubikey, self).authenticate(*args, **kwargs)
		
		if user and user.yubicokey_set.filter(enabled = True).count():
			return None
		else:
			return user