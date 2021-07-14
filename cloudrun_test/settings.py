"""
Django settings for cloudrun_test project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import io
import os

import environ
import google.auth
from google.cloud import secretmanager as sm

# Import the original settings from each template
from .basesettings import *

try:
    from .local import *
except ImportError:
    pass


# Pull django-environ settings file, stored in Secret Manager
SETTINGS_NAME = "cloudrun-test-settings"

_, project = google.auth.default()
client = sm.SecretManagerServiceClient()
name = f"projects/{project}/secrets/{SETTINGS_NAME}/versions/latest"
payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

env = environ.Env()
env.read_env(io.StringIO(payload))

# Setting this value from django-environ
SECRET_KEY = env("SECRET_KEY")

# Allow all hosts to access Django site
ALLOWED_HOSTS = ["*"]

# Default false. True allows default landing pages to be visible
DEBUG = env("DEBUG")

# Set this value from django-environ
DATABASES = {}

INSTALLED_APPS += ["storages"] # for django-storages
