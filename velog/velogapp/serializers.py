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


class SeriesSerializer(serializers.ModelSerializer):
    postNum = serializers.SerializerMethodField()
    #update_at, thumbnail
    def get_postNum(self, obj):
        return Post.objects.filter(series=obj.id).count()
    class Meta:
        model = Series
        fields = [
            'id',
            'series_name',
            'author',
            'postNum',
        ]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)
    series = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = [
            'pid',
            'series',
            'get_or_create_series',
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
            'url',
        ]
        write_only_field = ['create_tag',
                            'get_or_create_series'
                            ]

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
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = [
            'cid',
            'post',
            'author',
            'created_at',
            'content',
            'parent_comment',
            'comment_like_count',
        ]
        read_only_fields = ['post',
                            'author',
                            'comment_like_count',
                            ]
        model = Comment

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)


    class Meta:
        model = Post
        fields = [
            'pid',
            'series',
            'title',
            'tags',
            'author',
            'created_at',
            'updated_at',
            'content',
            'likes',
        ]

