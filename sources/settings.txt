--------
Settings
--------

The following settings are available:

.. _settings-YUBICO_USE_PASSWORD:

YUBICO_USE_PASSWORD
~~~~~~~~~~~~~~~~~~~

Defaults to true ``True`` and means that user will also need to enter his account password after entering the OTP.
If you want to allow user to only use his YubiKey to login, set this to ``False``.

.. _settings-YUBIKEY_PASSWORD_ATTEMPTS:

YUBIKEY_PASSWORD_ATTEMPTS
~~~~~~~~~~~~~~~~~~~~~~~~~

Defaults to true ``3`` and means how many times user can enter a wrong password before he needs to provide a new OTP.
This helps to prevent brute forces attacks when someone gets a valid token or steals user's session cookie.

Note that this setting only has an effect if ``YUBICO_USE_PASSWORD`` is set to ``True``.

YUBIKEY_SESSION_USER
~~~~~~~~~~~~~~~~~~~~

The name of the session key where the user object is saved. Defaults to ``yubicodjango_user``.

YUBIKEY_ATTEMPT_COUNTER
~~~~~~~~~~~~~~~~~~~~~~~

The name of the session key which holds the value of how many times user has entered the wrong password.
Defaults to ``yubicodjango_counter``.