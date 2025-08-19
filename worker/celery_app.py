#!/usr/bin/env python3
"""
Celery configuration for background tasks
"""

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('CELERY_CONFIG_MODULE', 'worker.celeryconfig')

# Create the celery app
celery_app = Celery('trading_bot')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
celery_app.config_from_object('worker.celeryconfig')

# Import tasks explicitly
celery_app.autodiscover_tasks(['worker.tasks'])

# Import tasks directly to ensure they're registered
import worker.tasks

@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
