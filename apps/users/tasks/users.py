from django.core import signing
from django.core.mail import send_mail
from apps.users.utils import generate_verification_url
from django.conf import settings
from apps.users.models import CustomUser
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_verification_url_to_email(email, user_id):

    url = generate_verification_url(user_id)

    send_mail(
        'URL for verification',
        url,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )


@shared_task
def delete_unverified_users():

    one_month_ago = timezone.now() - relativedelta(month=1)

    unverified_user_count, objs = CustomUser.objects \
        .filter(is_verified=False, created_at__gt=one_month_ago) \
        .delete()

    logger.info(f'Delete unverified users, date:{timezone.now().date()}, count:{unverified_user_count}')