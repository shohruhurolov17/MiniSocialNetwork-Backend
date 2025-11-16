from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from apps.articles.serializers import (
    ArticleDetailSerializer,
    ArticleCreateSerializer,
    ArticleCommentSerializer
)
from apps.articles.models import Article, ArticleLike, ArticleComment
from rest_framework import status
from apps.shared.response import CustomResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from collections import defaultdict
from django.db.models import Prefetch, F, Q
from apps.shared.pagination import CustomPagination
from rest_framework.generics import ListCreateAPIView
from apps.users.permissions import IsVerified


class ArticleListCreateView(APIView):

    permission_classes = (IsVerified, )
    pagination_class = CustomPagination

    def get_queryset(self):

        search = self.request.query_params.get('search')

        base_qs = Article.objects \
            .select_related('author') \
            .prefetch_related('likes') 
        
        if search:
            search_terms = search.split()
            query = Q()

            for search_term in search_terms:

                query &= (
                    Q(content__icontains=search_term) |
                    Q(title__icontains=search_term)
                )
            
            base_qs = base_qs.filter(query)
        
        return base_qs.order_by('-created_at')

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page',
                description='Page number',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='per_page',
                description='Page size',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='search',
                description='Search',
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR
            )
        ]
    )
    def get(self, request):

        data = defaultdict(
            lambda: {
                'username': None,
                'articles': []
            }
        )

        article_qs = self.get_queryset()
        
        paginator = self.pagination_class()

        paginated_qs = paginator.paginate_queryset(
            article_qs,
            request
        )
        
        for article in paginated_qs:

            likes = article.likes \
                .values(
                    'user_id',
                    full_name=F('user__full_name'),
                    username=F('user__username')
                )

            username = article.author.username

            if data[username]['username'] is None:
                data[username]['username'] = username
            
            data[username]['articles'].append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'likes': likes
            })
        
        grouped = list(data.values())

        return paginator.get_paginated_response(grouped)
        
    
    @extend_schema(request=ArticleCreateSerializer)
    def post(self, request):

        serializer = ArticleCreateSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():

            article = serializer.save()

            data = ArticleDetailSerializer(article).data

            return CustomResponse(data=data)
        
        else:

            error_message = str(serializer.errors)

            return CustomResponse(
                success=False,
                message=error_message,
                status=status.HTTP_400_BAD_REQUEST
            )


class ArticleDetailView(APIView):

    permission_classes = (IsVerified, )
    serializer_class = ArticleDetailSerializer

    def get_object(self):

        try:

            return Article.objects.get(id=self.kwargs['id'])
        
        except Article.DoesNotExist:

            raise NotFound('Article not found')
    
    def get(self, request, id):

        article = self.get_object()

        serializer = self.serializer_class(article)

        return CustomResponse(data=serializer.data)
    
    def patch(self, request, id):

        article = self.get_object()

        serializer = self.serializer_class(
            article,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return CustomResponse(data=serializer.data)

        else:

            error_message = str(serializer.errors)

            return CustomResponse(
                success=False,
                message=error_message,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request, id):

        article = self.get_object()

        article.delete()

        return CustomResponse(status=status.HTTP_204_NO_CONTENT)


class ArticleCommentListCreateView(ListCreateAPIView):

    permission_classes = (IsVerified, )
    serializer_class = ArticleCommentSerializer

    def get_object(self):

        try:

            return Article.objects \
                .get(id=self.kwargs['id'])
        
        except Article.DoesNotExist:
            raise NotFound('Article not found')
        
    def get_queryset(self):

        article = self.get_object()

        return ArticleComment.objects \
            .filter(article=article) \
            .select_related('article')
    
    def post(self, request, id):

        article = self.get_object()

        serializer = self.serializer_class(
            data=request.data,
            context={
                'article': article,
                'request': request
            }
        )

        if serializer.is_valid():

            serializer.save()

            return CustomResponse(message='Comment accepted')
        
        else:

            error_message = str(serializer.errors)

            return CustomResponse(
                success=False,
                message=error_message,
                status=status.HTTP_400_BAD_REQUEST
            )


class LikeArticleView(APIView):

    def get_object(self):

        user = self.request.user

        try:

            return Article.objects \
                .exclude(author=user) \
                .get(id=self.kwargs['id'])
        
        except Article.DoesNotExist:
            raise NotFound('Article not found')
    
    def post(self, request, id):

        article = self.get_object()

        obj, created = ArticleLike.objects \
            .get_or_create(
                user=request.user,
                article=article
            )
        
        return CustomResponse(
            data={
                'is_like': created
            }
        )