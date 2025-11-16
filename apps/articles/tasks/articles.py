from dateutil.relativedelta import relativedelta
from django.utils import timezone
from apps.articles.models import Article
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def delete_expired_articles():

    one_month_ago = timezone.now() - relativedelta(month=1)

    deleted_article_count, objs = Article.objects \
        .filter(created_at__gt=one_month_ago) \
        .delete()
    
    logger.info(f'Delete expired articles, date:{timezone.now().date()}, count:{deleted_article_count}')



