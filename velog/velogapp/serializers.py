from rest_framework import serializers
from .models import *
from django.db.models import Q

# is_private filter
class FilterPrivateListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context['request'].user.is_authenticated:
            data = data.filter(Q(author=self.context['request'].user) |
                                       Q(is_private=False)
                                       )
        else:
            data = data.filter(is_private=False)
        return super(FilterPrivateListSerializer, self).to_representation(data)

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

class SeriesCreateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Series
        fields = [
            'id',
            'author',
            'series_name',
            'url',
            'update',
        ]

class SeriesSerializer(serializers.ModelSerializer):
    postNum = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)

    def get_postNum(self, obj):
        return Post.objects.filter(series=obj.id).count()
    class Meta:
        model = Series
        fields = [
            'id',
            'series_name',
            'url',
            'update',
            'author',
            'postNum',
        ]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
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
            'url',
        ]
        write_only_field = ['create_tag',]

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
            'url',
        ]
        list_serializer_class = FilterPrivateListSerializer

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



class SeriesDetailSerializer(serializers.ModelSerializer):
    postList = PostListSerializer(many=True, read_only=True, source='post_set')
    # 비공개 post 처리 필요
    postNum = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)

    def get_postNum(self, obj):
        return Post.objects.filter(series=obj.id).count()

    class Meta:
        model = Series
        fields = [
            'id',
            'series_name',
            'update',
            'author',
            'postNum',
            'postList',
        ]