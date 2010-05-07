from django.contrib import admin

from models import YubicoKey

class YubicoKeyAdmin(admin.ModelAdmin):
	list_display = ('user', 'device_id', 'client_id', 'secret_key', 'enabled')
	search_fields = ['user', 'device_id', 'client_id']

admin.site.register(YubicoKey, YubicoKeyAdmin)