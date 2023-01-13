from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User


class UserSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "name",
            "gender",
            "birthday",
            "profile_image",
            "introduction",
        ]
        read_only_fields = [
            "email",
            "id",
        ]


class UserLoginSerializer(LoginSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    # username = None


class CustomRegisterSerializer(RegisterSerializer):
    # username = None
    username = serializers.CharField(max_length=100)
    birthday = serializers.DateField()
    name = serializers.CharField(max_length=100)
    gender = serializers.ChoiceField(choices=User.Gender.choices)
    profile_image = serializers.ImageField(default="")
    introduction = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "birthday": self.validated_data.get("birthday", ""),
            "name": self.validated_data.get("name", ""),
            "gender": self.validated_data.get("gender", ""),
            "profile_image": self.validated_data.get("profile_image", ""),
            "introduction": self.validated_data.get("introduction", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)

        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except ValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.birthday = self.validated_data.get("birthday", "")
        user.name = self.validated_data.get("name", "")
        user.gender = self.validated_data.get("gender", "")
        user.profile_image = self.validated_data.get("profile_image", "")
        user.introduction = self.validated_data.get("introduction", "")
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
