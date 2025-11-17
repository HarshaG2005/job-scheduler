# from celery import Celery
# import os
# from dotenv import load_dotenv

# load_dotenv()

# REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# app = Celery(
#     'job_scheduler',
#     broker=REDIS_URL,
#     backend=REDIS_URL
# )

# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='UTC',
#     enable_utc=True,
# ) 

# from app.workers import notification_tasks
from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise RuntimeError("REDIS_URL environment variable not set")

# Handle Upstash Redis SSL (rediss://)
broker_url = REDIS_URL
backend_url = REDIS_URL

# Add SSL parameters if using rediss://
if REDIS_URL.startswith("rediss://"):
    # Upstash requires specific SSL settings
    broker_use_ssl = {
        'ssl_cert_reqs': None  # Don't verify SSL cert for Upstash
    }
    redis_backend_use_ssl = broker_use_ssl
else:
    broker_use_ssl = None
    redis_backend_use_ssl = None

app = Celery(
    'job_scheduler',
    broker=broker_url,
    backend=backend_url
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_use_ssl=broker_use_ssl,
    redis_backend_use_ssl=redis_backend_use_ssl,
    # Upstash connection pool settings
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
)

from app.workers import notification_tasks