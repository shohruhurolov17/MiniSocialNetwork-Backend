from django.urls import path
from apps.articles.views import (
    ArticleDetailView,
    ArticleCommentListCreateView,
    LikeArticleView,
    ArticleListCreateView
)

urlpatterns = [
    path('articles/', ArticleListCreateView.as_view(), name='article_list_create'),
    path('articles/<uuid:id>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/<uuid:id>/comments/', ArticleCommentListCreateView.as_view(), name='add_article_comment'),
    path('articles/<uuid:id>/like/', LikeArticleView.as_view(), name='like_article')
]