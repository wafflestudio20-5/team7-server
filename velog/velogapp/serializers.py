from rest_framework import serializers
from .models import Comment
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('post', 'created_by', 'created_at', 'content', 'parent_comment')
        model = Comment

