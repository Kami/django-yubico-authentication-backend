---
FAQ
---

Does this module work with Django 1.2?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes, this module is tested and should work fine with Django 1.2.

Does this module support offline authentication?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
No, this module depends on the yubico-python_ module and only supports the safest, online OTP authentication against Yubico or your own validation servers.

Can multiple users use the same YubiKey to log in?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Yes, the only requirement is that your website account usernames are unique.

This is required because user must enter his username + OTP to log in.

If you want more users to share the same YubiKey, it would be the safest to enable the ``YUBICO_USE_PASSWORD`` setting (you can read more about the available settings at the :doc:`settings` page).

How can I customize the login templates?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can customize the login templates by copying the ``login.html`` and ``password.html`` files from the ``django_yubico/templates/django_yubico/`` folder to your Django application templates folder and editing them (you must preserve the directory structure or change the path to the template files in ``django_yubico/views.py``).

.. _yubico-python: http://github.com/Kami/python-yubico-client