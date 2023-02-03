from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Series)

# Register your models here.
