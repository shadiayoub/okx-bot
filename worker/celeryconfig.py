#!/usr/bin/env python3
"""
Celery configuration
"""

import os

# Broker settings
broker_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Result backend
result_backend = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Task serialization
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
timezone = 'UTC'
enable_utc = True

# Task routing
task_routes = {
    'worker.tasks.*': {'queue': 'default'},
}

# Worker settings
worker_prefetch_multiplier = 1
worker_max_tasks_per_child = 1000

# Task settings
task_always_eager = False
task_eager_propagates = True

# Result settings
result_expires = 3600  # 1 hour

# Beat settings (for periodic tasks)
beat_schedule = {
    'retrain-models': {
        'task': 'worker.tasks.retrain_models',
        'schedule': 86400.0,  # 24 hours
    },
}
