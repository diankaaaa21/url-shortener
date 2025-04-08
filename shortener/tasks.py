import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def log_url_creation(original_url, short_token):
    logger.info(f"Created short URL: {short_token} - {original_url}")
