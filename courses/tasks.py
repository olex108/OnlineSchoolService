import logging

from celery import shared_task
from django.core.mail import send_mail

from config.settings import BASE_URL, EMAIL_HOST_USER
from courses.models import Course


logger = logging.getLogger("celery_tasks")


@shared_task
def mailing_to_course_subscribers(course_pk: int) -> None:
    """
    Task for sending email to subscribers of course

    :param course_pk: pk of Course model
    """

    course = Course.objects.get(id=course_pk)
    subscribers_queryset = course.subscription_set.filter(subscription=True)
    logger.info(f"Update course: {course.name} - mailing for subscribers count: {subscribers_queryset.count()}")
    for subscription in subscribers_queryset:
        try:
            send_mail(
                subject=f"Обновление курса {course.name}",
                message=f"Курс {course.name} на который вы подписаны обновлен. Для просмотра изменений зайдите на страницу курса '{BASE_URL}course/{course.id}/'",
                from_email=EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
            )
        except Exception as e:
            print(f"User: {subscription.user.email} - {e}")
            logger.error(f"User: {subscription.user.email} - {e}")
