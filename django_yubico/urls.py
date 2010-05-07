from django.conf.urls.defaults import *

from views import login, password

urlpatterns = patterns('',
    url(r'^login', login, name = 'yubico_django_login'),
    url(r'^password', password, name = 'yubico_django_password'),
)