# myproject/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import sentry_sdk

sentry_sdk.init(
    dsn="https://0ab1dc58df87ac8b44e16e2bf835be1f@o4508296085372928.ingest.us.sentry.io/4508296098021376",
)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CeleryLab.settings')

app = Celery('CeleryLab')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.broker_connection_retry_on_startup = True
