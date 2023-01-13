from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    class Gender(models.TextChoices):
        FEMALE = "F", _("Female")
        MALE = "M", _("Male")
        OTHER = "O", _("Other")

    username = models.CharField(
        _("username"),
        max_length=100,
        unique=True,
    )
    first_name = None
    last_name = None
    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    birthday = models.DateField(default="1900-01-01")
    name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(
        choices=Gender.choices, default=Gender.OTHER, max_length=10
    )
    profile_image = models.ImageField(upload_to="authentication/pictures", blank=True)
    introduction = models.CharField(max_length=100, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"<User {self.email}>"
