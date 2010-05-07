from django.db import models
from django.contrib.auth.models import User

class YubicoKey(models.Model):
	device_id = models.CharField(max_length = 12)
	client_id = models.IntegerField()
	secret_key = models.CharField(max_length = 80, blank = True)
	user = models.ForeignKey(User)
	enabled = models.BooleanField(default = True)
	
	class Meta:
		verbose_name = 'Yubico YubiKey'
		verbose_name_plural = 'Yubico YubiKeys'