from rest_framework import serializers
from .models import *

class TagSerializer(serializers.ModelSerializer):
    postCount = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)
    def get_postCount(self, obj):
        return Post.objects.filter(tags=obj.id).count()
    class Meta:
        model = Tag
        fields = ['id',
                  'tag_name',
                  'author',
                  'postCount',
                  ]

class TagCountSerializer(serializers.ModelSerializer):
    postCount = serializers.SerializerMethodField()
    def get_postCount(self, obj):
        return Post.objects.filter(tags__tag_name=obj['tag_name']).count()
    class Meta:
        model = Tag
        fields = [
                  'tag_name',
                  'postCount',
                  ]


class SeriesSerializer(serializers.ModelSerializer):
    postNum = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)
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
    author = serializers.StringRelatedField(read_only=True)
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
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(read_only=True)
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        return Comment.objects.filter(post__pid=obj.pid).count()

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
            'comments',
        ]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

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
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    is_active = serializers.SerializerMethodField(default=False)

    def get_is_active(self, obj):
        try:
            if self.context['request'].user in obj.like_user.all():
                return True
            else:
                return False
        except:
            return False

    class Meta:
        model = Post
        fields = [
            'pid',
            'series',
            'title',
            'tags',
            'author',
            'url',
            'created_at',
            'updated_at',
            'content',
            'likes',
            'is_active',
            'comments',
        ]

