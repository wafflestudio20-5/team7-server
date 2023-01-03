from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)

class Comment(models.Model):
    #Post class
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Re-comment
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content
