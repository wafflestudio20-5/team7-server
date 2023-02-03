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
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        try:
            return Post.objects.get(series=obj.id, series_order=1).thumbnail.url
        except:
            return None

    def get_postNum(self, obj):
        return Post.objects.filter(series=obj.id).count()
    class Meta:
        model = Series
        fields = [
            'id',
            'series_name',
            'url',
            'photo',
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
            'series_order',
        ]
        write_only_fields = ['create_tag',]
        read_only_fields = ['series_order',]
        
    def create(self, validated_data):
        instance = Post.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        
        for image_data in image_set.getlist('image'):
            PostImage.objects.create(post=instance, image=image_data)

        return instance
    

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
        #list_serializer_class = FilterPrivateListSerializer

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


class SeriesPostSerializer(serializers.ModelSerializer):
    post = PostListSerializer(source='*', read_only=True)
    class Meta:
        model = Post
        fields = [
            'series_order',
            'post',
        ]
        list_serializer_class = FilterPrivateListSerializer

class SeriesDetailSerializer(serializers.ModelSerializer):
    postList = SeriesPostSerializer(many=True, read_only=True, source='post_set')
    postNum = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True)
    photo = serializers.SerializerMethodField()

    def get_postNum(self, obj):
        return Post.objects.filter(series=obj.id).count()
    def get_photo(self, obj):
        try:
            return Post.objects.get(series=obj.id, series_order=1).thumbnail.url
        except:
            return None

    class Meta:
        model = Series
        fields = [
            'id',
            'series_name',
            'photo',
            'update',
            'author',
            'postNum',
            'postList',
        ]

        def update(self, instance, validated_data):
            if 'postList' in validated_data:
                nested_serializer = self.fields['postList']
                nested_instance = instance.postList
                nested_data = validated_data.pop('postList')
                nested_serializer.update(nested_instance, nested_data)
            return super(SeriesDetailSerializer, self).update(instance, validated_data)

class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.PrimaryKeyRelatedField(read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')
    is_active = serializers.SerializerMethodField(default=False)
    series = SeriesDetailSerializer(required=False, read_only=True)
    prev_post = serializers.SerializerMethodField()
    next_post = serializers.SerializerMethodField()
    def get_prev_post(self, obj):
        if obj.series:
            try:
                prev_post = Post.objects.get(series=obj.series, series_order=obj.series_order-1)
                return PostListSerializer(prev_post).data
            except:
                pass
        else:
            try:
                postset = Post.objects.filter(series=None, author=obj.author).order_by('created_at')
                obj_index = postset.filter(created_at__lt=obj.created_at).count()
                if obj_index > 0:
                    prev_post = postset[obj_index - 1]
                else:
                    prev_post = None
                return PostListSerializer(prev_post).data
            except IndexError:
                pass



    def get_next_post(self, obj):
        if obj.series:
            try:
                prev_post = Post.objects.get(series=obj.series, series_order=obj.series_order + 1)
                return PostListSerializer(prev_post).data
            except:
                return None
        else:
            try:
                postset = Post.objects.filter(series=None, author=obj.author).order_by('created_at')
                obj_index = postset.filter(created_at__lt=obj.created_at).count()
                next_post = postset[obj_index + 1]
                return PostListSerializer(next_post).data
            except IndexError:
                pass


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
            'preview',
            'thumbnail',
            'created_at',
            'updated_at',
            'content',
            'likes',
            'is_active',
            'comments',
            'is_private',
            'prev_post',
            'next_post',
        ]
