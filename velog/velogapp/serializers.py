from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, 'author': self.context['request'].user}

    class Meta:
        model = Post
        fields = [
            'pid',
            'series',
            'title',
            'author',
            'created_at',
            'updated_at',
            'thumbnail',
            'preview',
            'content',
            'is_private',
            'tags',
        ]
        

class PostListSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    like_count = serializers.PrimaryKeyRelatedField(read_only=True)
    
    
    # comment_count 기능

    class Meta:
        model = Post
        fields = [
            'pid',
            'title',
            'thumbnail',
            'preview',
            'author',
            'created_at',
            'updated_at',
            'like_count',

        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    like_count = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'pid',
            'title',
            'tags',
            'author',
            'created_at',
            'updated_at',
            'content',
            'like_count',
        ]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        field = ['tag_name']
        

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'cid',
            'post',
            'author',
            'created_at',
            'content',
            'parent_comment'
        ]
        read_only_fields = ['post', 'author']
        model = Comment

