from rest_framework import serializers

from .models import *


class PostSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        return {**internal_value, "created_by": self.context["request"].user}

    class Meta:
        model = Post
        fields = [
            "id",
            "series",
            "title",
            "created_by",
            "created_at",
            "updated_at",
            "thumbnail",
            "preview",
            "description",
            "is_private",
            "tags",
        ]


class PostListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    like_count = serializers.PrimaryKeyRelatedField(read_only=True)

    # comment_count 기능

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "thumbnail",
            "preview",
            "created_by",
            "created_at",
            "updated_at",
            "like_count",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    like_count = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "tags",
            "created_by",
            "created_at",
            "updated_at",
            "description",
            "like_count",
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        field = ["tag_name"]
