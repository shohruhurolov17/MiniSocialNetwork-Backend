from django.db import models 
from apps.shared.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Article(BaseModel):

    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='articles'
    )

    title = models.TextField()

    content = models.TextField()

    class Meta:

        db_table = 'articles'
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ('-created_at', )


class ArticleLike(BaseModel):

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='article_likes'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:

        db_table = 'article_likes'
        verbose_name = _('Article like')
        verbose_name_plural = _('Article likes')
        ordering = ('-created_at', )


class ArticleComment(BaseModel):

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='article_comments'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField()

    class Meta:

        db_table = 'article_comments'
        verbose_name = _('Article comment')
        verbose_name_plural = _('Article comments')
        ordering = ('-created_at', )