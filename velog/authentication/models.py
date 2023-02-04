from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(
        _("username"),
        max_length=100,
        unique=True,
    )
    first_name = None
    last_name = None
    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    name = models.CharField(max_length=100, blank=True)
    velog_name = models.CharField(max_length=100, blank=True)
    mail = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    homepage = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="authentication/pictures", blank=True, null=True, default='default.png')
    introduction = models.CharField(max_length=100, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username}"
