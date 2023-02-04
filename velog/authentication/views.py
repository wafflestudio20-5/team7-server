from json.decoder import JSONDecodeError

import requests

from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.facebook import views as facebook_view
from allauth.socialaccount.providers.github import views as github_view
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialConnectView, SocialLoginView
from dj_rest_auth.views import UserDetailsView
from django.conf import settings
from django.http import JsonResponse, QueryDict, FileResponse
from django.shortcuts import redirect
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework.permissions import AllowAny
from velogapp.models import Post, Tag, Series, Comment
from .models import User
from .serializers import UserSerializer
from .permissions import IsCreator

BASE_URL = "https://api.7elog.store/api/v1/"

import logging
logger = logging.getLogger(__name__)

# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
# from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter

# BASE_URL = "https://api.7elog.store"

GOOGLE_CALLBACK_URI = BASE_URL + "accounts/google/login/callback/"
KAKAO_CALLBACK_URI = BASE_URL + "accounts/kakao/login/callback/"
GITHUB_CALLBACK_URI = BASE_URL + "accounts/github/login/callback/"
FACEBOOK_CALLBACK_URI = BASE_URL + "accounts/facebook/login/callback/"

state = getattr(settings, "STATE")

def MediaProfileView(request, filename:str):
    try:
        base_url = 'media/authentication/pictures/'
        img = open(base_url + filename, 'rb')
        print(filename)
        response = FileResponse(img)
        return response
    except:
        return JsonResponse(data={"error": "no url"}, status=status.HTTP_400_BAD_REQUEST)

class UserListUpdateView(UserDetailsView):
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        new_username = request.data.get("username", None)
        if new_username == request.user.username:
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
                request.data.pop('username')
                request.data._mutable = False
            else:
                request.data.pop('username')
            kwargs['partial'] = True
        profile = request.data.get("profile_image", None)
        if profile:
            pass
        else:
            profile = request.user.profile_image
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
            request.data['profile_image'] = profile
            request.data._mutable = False
        else:
            request.data['profile_image'] = profile
        return super().update(request, *args, **kwargs)


class UsernameView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset().get(username=kwargs['username'])
            serializer = self.serializer_class(queryset)
            return Response(serializer.data)
        except:
            return Response(data={f"message": f"There is no user {kwargs['username']}"}, status=status.HTTP_404_NOT_FOUND)


class UserDestroyView(generics.DestroyAPIView):
    permission_classes = [IsCreator | permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        for post in Post.objects.filter(author=instance):
            post.delete()
        for comment in Comment.objects.filter(author=instance):
            comment.delete()
        for tag in Tag.objects.filter(author=instance):
            tag.delete()
        for series in Series.objects.filter(author=instance):
            series.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


def google_login(request):
    """
    Code Request
    """
    scope = "https://www.googleapis.com/auth/userinfo.email"
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    return redirect(
        f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}"
    )


def google_callback(request):
    client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
    client_secret = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")
    code = request.GET.get("code")
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    email_req = requests.get(
        f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
    )
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse(
            {"err_msg": "failed to get email"}, status=status.HTTP_400_BAD_REQUEST
        )
    email_req_json = email_req.json()
    email = email_req_json.get("email")
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 google이 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "google":
            return JsonResponse(
                {"err_msg": f"user is already signed up with {social_user.provider}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 Google로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        # accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        accept_json = accept.json()
        # accept_json.pop('user', None)
        return JsonResponse(accept_json)


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client


def kakao_login(request):
    rest_api_key = getattr(settings, "KAKAO_CLIENT_ID")
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )


def kakao_callback(request):
    rest_api_key = getattr(settings, "KAKAO_CLIENT_ID")
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    profile_json = profile_request.json()
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    kakao_account = profile_json.get("kakao_account")
    """
    kakao_account에서 이메일 외에
    카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
    print(kakao_account) 참고
    """
    email = kakao_account.get("email")
    kakao_account["username"] = kakao_account.get("profile", {}).get("nickname")
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "kakao":
            return JsonResponse(
                {"err_msg": f"user is already signed up with {social_user.provider}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 Google로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        # accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        # accept_json.pop('user', None)
        return JsonResponse(accept_json)


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI


def github_login(request):
    client_id = getattr(settings, "GH_CLIENT_ID")
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={GITHUB_CALLBACK_URI}"
    )


def github_callback(request):
    client_id = getattr(settings, "GH_CLIENT_ID")
    client_secret = getattr(settings, "GH_SECRET_KEY")
    code = request.GET.get("code")
    """
    Access Token Request
    """
    token_req = requests.post(
        f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}&accept=&json&redirect_uri={GITHUB_CALLBACK_URI}&response_type=code",
        headers={"Accept": "application/json"},
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    user_req = requests.get(
        f"https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_json = user_req.json()
    error = user_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    email = user_json.get("email")
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        # 기존에 가입된 유저의 Provider가 github가 아니면 에러 발생, 맞으면 로그인
        # 다른 SNS로 가입된 유저
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "github":
            return JsonResponse(
                {"err_msg": f"user is already signed up with {social_user.provider}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 기존에 github로 가입된 유저
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/github/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        return JsonResponse(accept_json)


class GithubLogin(SocialLoginView):
    """
    If it's not working
    You need to customize GitHubOAuth2Adapter
    use header instead of params
    -------------------
    def complete_login(self, request, app, token, **kwargs):
        params = {'access_token': token.token}
    TO
    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token)}
    -------------------
    """

    adapter_class = github_view.GitHubOAuth2Adapter
    callback_url = GITHUB_CALLBACK_URI
    client_class = OAuth2Client


def facebook_login(request):
    client_id = getattr(settings, "FACEBOOK_CLIENT_ID")
    return redirect(
        f"https://facebook.com/v13.0/dialog/oauth?client_id={client_id}&grant_type=authorization_code&redirect_uri={FACEBOOK_CALLBACK_URI}&state={state}"
    )


def facebook_callback(request):
    client_id = getattr(settings, "FACEBOOK_CLIENT_ID")
    client_secret = getattr(settings, "FACEBOOK_SECRET_KEY")
    code = request.GET.get("code")
    """
    Access Token Request
    """
    token_req = requests.get(
        f"https://graph.facebook.com/v13.0/oauth/access_token?client_id={client_id}&redirect_uri={FACEBOOK_CALLBACK_URI}&client_secret={client_secret}&code={code}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    """
    Email Request
    """
    user_req = requests.get(
        f"https://graph.facebook.com/v13.0/me?fields=id,name,picture,email",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_json = user_req.json()
    error = user_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    email = user_json.get("email")
    """
    Signup or Signin Request
    """
    try:
        user = User.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse(
                {"err_msg": "email exists but not social user"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if social_user.provider != "facebook":
            return JsonResponse(
                {"err_msg": f"user is already signed up with {social_user.provider}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/facebook/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        # accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except User.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}accounts/facebook/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
        # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴
        accept_json = accept.json()
        # accept_json.pop('user', None)
        return JsonResponse(accept_json)


class FacebookLogin(SocialLoginView):
    adapter_class = facebook_view.FacebookOAuth2Adapter
    client_class = OAuth2Client
    callback_url = FACEBOOK_CALLBACK_URI

class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect('/') # 인증성공

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        

        logger.info(email_confirmation)
        print(email_confirmation)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
                email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect('/') # 인증실패
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs
