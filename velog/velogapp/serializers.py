from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    postCount = serializers.SerializerMethodField()
    def get_postCount(self, obj):
        return Post.objects.filter(tags=obj.id).count()
    class Meta:
        model = Tag
        fields = ['id',
                  'tag_name',
                  'postCount',
                  ]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)

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
            'create_tag',
            'tags',
        ]
        write_only_field = ['create_tag']

class PostListSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(read_only=True)
    
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
            'likes',

        ]

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

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)

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
            'likes',
        ]

