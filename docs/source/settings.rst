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

YUBICO_MULTI_MODE
~~~~~~~~~~~~~~~~~
Defaults to ``False``.

If set to ``True`` user will need to enter ``YUBICO_MULTI_NUMBER`` number of OTPs which were generated in the ``YUBICO_MULTI_TIMEOUT`` seconds long time window for a successful validation.

YUBICO_MULTI_NUMBER
~~~~~~~~~~~~~~~~~~~

Defaults to ``3``.

The number of OTPs user will need to enter when multi mode is enabled.

*Note: This setting is only applicable is YUBICO_MULTI_MODE is set to True.*

YUBICO_MULTI_TIMEOUT
~~~~~~~~~~~~~~~~~~~~

Defaults to ``10``.

How many seconds can pass between the time when the first and the last OTP is generated.

*Note: This setting is only applicable is YUBICO_MULTI_MODE is set to True.*