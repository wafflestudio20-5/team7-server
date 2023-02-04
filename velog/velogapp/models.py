from authentication.models import User
from django.db import models
from authentication.models import User


class Series(models.Model):
    series_name = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    url = models.CharField(max_length=100, null=True, unique=True)
    update = models.DateTimeField(auto_now=True)


class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    series = models.ForeignKey(Series, on_delete=models.PROTECT, null=True)
    thumbnail = models.ImageField(null=True, default='media/default.png')
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
    view_user = models.ManyToManyField(User, related_name='user_who_viewed', blank=True)
    create_tag = models.CharField(max_length=200, null=True)
    get_or_create_series = models.CharField(max_length=100, null=True)
    url = models.CharField(max_length=100, null=True)
    series_order = models.IntegerField(null=True)

    
def image_upload_path(instance, filename):
    return f'{filename}'


class PostImage(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(null=False)

    def __int__(self):
        return self.id

    class Meta:
        db_table = 'velogapp_postimage'
    
    
class Tag(models.Model):
    tag_name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.PROTECT)

class Comment(models.Model):
    #Post class
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # like-comment
    comment_like_count = models.PositiveIntegerField(default=0)
    comment_like_user = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    #Re-comment
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

