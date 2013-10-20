try:
    from django.conf.urls import patterns, url
except ImportError:
    # Django < 1.4
    from django.conf.urls.defaults import patterns, url

from views import login, password

urlpatterns = patterns(
    '',
    url(r'^login', login, name='yubico_django_login'),
    url(r'^password', password, name='yubico_django_password'),
)
