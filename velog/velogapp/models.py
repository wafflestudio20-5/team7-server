from django.db import models
from authentication.models import User
from django.utils.translation import gettext_lazy as _


class Series(models.Model):
    series_name = models.CharField(max_length=100)

class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    series = models.ForeignKey(Series, on_delete=models.PROTECT, null=True)
    thumbnail = models.ImageField(null=True)
    title = models.TextField()
    preview = models.CharField(max_length=150, null=True)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    like_user = models.ManyToManyField(User, related_name='user_who_liked', blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    hits = models.PositiveIntegerField(default=0)

class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

class ReadingList(models.Model):
    posts_liked = models.ManyToManyField(Post, related_name='posts_liked')
    posts_viewed = models.ManyToManyField(Post, related_name='posts_viewed')

class Comment(models.Model):
    #Post class
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Re-comment
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

# Create your models here.
