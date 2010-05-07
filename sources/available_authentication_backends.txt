---------------------------------
Available authentication backends
---------------------------------

This module offers the following three authentication backends.

.. _authentication_backends-YubicoBackend:

YubicoBackend
~~~~~~~~~~~~~

This is a base backend which must be enabled if you want to use the YubiKey authentication.

You can enable it by putting the following lines to your ``settings.py`` file::

   AUTHENTICATION_BACKENDS = (
		'django_yubico.backends.YubicoBackend',
	)

If you still want to allow other users without a YubiKey to log in, you must enable the ``django.contrib.auth.backends.ModelBackend`` as well::

   AUTHENTICATION_BACKENDS = (
		'django_yubico.backends.YubicoBackend',
		'django.contrib.auth.backends.ModelBackend',
	)

.. _authentication_backends-YubicoBackendStaff:

YubicoBackendStaff
~~~~~~~~~~~~~~~~~~

This backend should be used in combination with the ``YubicoBackend`` backend and requires all the staff and super users to use the YubiKey to log in (normal users with or without a YubiKey will still be able to log in using their password)::

   AUTHENTICATION_BACKENDS = (
   		'django_yubico.backends.YubicoBackend',
   		'django_yubico.backends.YubicoBackendStaff',
   	)
	
.. _authentication_backends-YubicoBackendRequireYubikey:

YubicoBackendRequireYubikey
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This backend should also be used in combination with the ``YubicoBackend`` backend and requires **all** the users with at least one **active** / **enabled** YubiKey to log in using the YubiKey::

   AUTHENTICATION_BACKENDS = (
   		'django_yubico.backends.YubicoBackend',
   		'django_yubico.backends.YubicoBackendRequireYubikey',
   	)