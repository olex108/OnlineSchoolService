import logging

from celery import shared_task
from django.utils import timezone

from users.models import User


logger = logging.getLogger("celery_tasks")


@shared_task
def ban_inactive_users() -> None:
    users = User.objects.filter(is_active=True, last_login__lt=timezone.now() - timezone.timedelta(days=31))
    logger.info(f"{len(users)} users banned")
    for user in users:
        user.is_active = False
        user.save()
