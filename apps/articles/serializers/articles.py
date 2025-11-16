from rest_framework import serializers
from apps.articles.models import Article, ArticleComment, ArticleLike
import re
from typing import Dict


class ArticleCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = (
            'title',
            'content'
        )
    
    def validate_content(self, val):

        if len(val) >= 1000:

            raise serializers.ValidationError('Content must be shorter than 1000 characters')
    
        if not re.match(
            r'^[A-Za-zА-Яа-яЁё\s]{6,1000}$',
            val
        ):
            raise serializers.ValidationError('Content may contain only Latin/Cyrillic letters and spaces')

        return val
    
    def validate_title(self, val):

        if len(val) <= 5 or len(val) >= 1000:

            raise serializers.ValidationError('Title must be longer than 5 and shorter than 1000 characters')
    
        if not re.match(
            r'^[A-Za-zА-Яа-яЁё\s]{6,1000}$',
            val
        ):
            raise serializers.ValidationError('Title may contain only Latin/Cyrillic letters and spaces')

        return val
    
    def create(self, validated_data):

        author = self.context['request'].user

        validated_data['author'] = author

        return Article.objects.create(**validated_data)


class ArticleDetailSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = (
            'id',
            'title',
            'content',
            'author',
            'created_at',
            'updated_at'
        )
    
    def get_author(self, instance) -> Dict:

        return {
            'id': instance.author.id,
            'full_name': instance.author.full_name,
            'username': instance.author.username
        }


class ArticleCommentSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()

    class Meta:

        model = ArticleComment
        read_only_fields = (
            'user',
        )
        fields = (
            'id',
            'user',
            'text',
            'created_at'
        )
    
    def get_user(self, instance) -> Dict:

        return {
            'id': instance.user.id,
            'full_name': instance.user.full_name,
            'username': instance.user.username
        }
    
    def create(self, validated_data):

        user = self.context['request'].user
        article = self.context['article']

        validated_data.update({
            'user': user,
            'article': article
        })

        return ArticleComment.objects.create(**validated_data)


class ArticleLikeSerializer(serializers.ModelSerializer):

    class Meta:

        model = ArticleLike
        fields = (
            'id',
            'user',
            'article'
        )