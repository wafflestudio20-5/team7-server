from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserSerializer(UserDetailsSerializer):
    profile_image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "name",
            "profile_image",
            "introduction",
            "mail",
            "github",
            "twitter",
            "facebook",
            "homepage",
            "velog_name",
            "about",
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

    username = None


class CustomRegisterSerializer(RegisterSerializer):
    # username = None
    username = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    profile_image = serializers.ImageField(default="")
    introduction = serializers.CharField(max_length=100)

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "velog_name": self.validated_data.get("username", "") + ".log",
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
            "name": self.validated_data.get("name", ""),
            "profile_image": self.validated_data.get("profile_image", ""),
            "introduction": self.validated_data.get("introduction", ""),
            "mail": self.validated_data.get("mail", ""),
            "github": self.validated_data.get("github", ""),
            "twitter": self.validated_data.get("twitter", ""),
            "facebook": self.validated_data.get("facebook", ""),
            "homepage": self.validated_data.get("homepage", ""),
            "about": self.validated_data.get("about", ""),
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
        user.velog_name = self.validated_data.get("username", "") + ".log"
        user.name = self.validated_data.get("name", "")
        user.profile_image = self.validated_data.get("profile_image", "")
        user.introduction = self.validated_data.get("introduction", "")
        user.mail = self.validated_data.get("mail", "")
        user.github = self.validated_data.get("github", "")
        user.twitter = self.validated_data.get("twitter", "")
        user.facebook = self.validated_data.get("facebook", "")
        user.homepage = self.validated_data.get("homepage", "")
        user.about = self.validated_data.get("about", "")
        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs["refresh_token"])
        data = {"access_token": str(refresh.access_token)}

        return data
