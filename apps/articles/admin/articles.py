from django.contrib import admin
from apps.articles.models import (
    Article,
    ArticleComment,
    ArticleLike
)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
    )
    autocomplete_fields = (
        'author',
    )

    search_fields = (
        'id',
        'title',
        'content'
    )


@admin.register(ArticleLike)
class ArticleLikeAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
    )
    autocomplete_fields = (
        'user',
        'article'
    )


@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
    )

    autocomplete_fields = (
        'user',
        'article'
    )