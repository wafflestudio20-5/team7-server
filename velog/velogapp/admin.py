from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Tag)
admin.register(Comment)

# Register your models here.
