from djangoboys.settings.base import *

# Speeding up our tests
# https://docs.djangoproject.com/en/3.1/topics/testing/overview/#speeding-up-the-tests

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Ensure we're using local email backend when testing, and therefore not sending emails outside
# https://docs.djangoproject.com/en/3.1/topics/email/#in-memory-backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
