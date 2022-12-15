from djangoboys.settings.base import INSTALLED_APPS, MIDDLEWARE

ALLOWED_HOSTS = ["127.0.0.1"]

DEVELOPMENT_APPS = ["django_extensions", "django_browser_reload"]
DEVELOPMENT_MIDDLEWARES = ["django_browser_reload.middleware.BrowserReloadMiddleware"]

INSTALLED_APPS += DEVELOPMENT_APPS
MIDDLEWARE += DEVELOPMENT_MIDDLEWARES
