from allauth.account.views import ConfirmEmailView
from authentication import views
from dj_rest_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
    UserDetailsView,
)
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


urlpatterns = [
    path("login/", LoginView.as_view(), name='rest_login'),
    path("logout/", LogoutView.as_view(), name='rest_logout'),
    path("user/", views.UserListUpdateView.as_view(), name="user_detail"),
    path("user/@<str:username>", views.UsernameView.as_view(), name="username_view"),
    path("user/delete/@<str:username>", views.UserDestroyView.as_view(), name="user_delete"),
    path("signup/", RegisterView.as_view(), name="account_signup"),
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path(
        "signup/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<uid>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view()),
    path("google/login/", views.google_login, name="google_login"),
    path("google/login/callback/", views.google_callback, name="google_callback"),
    path(
        "google/login/finish/",
        views.GoogleLogin.as_view(),
        name="google_login_todjango",
    ),
    path("facebook/login/", views.facebook_login, name="facebook_login"),
    path("facebook/login/callback/", views.facebook_callback, name="facebook_callback"),
    path(
        "facebook/login/finish/",
        views.FacebookLogin.as_view(),
        name="facebook_login_todjango",
    ),
    path("github/login/", views.github_login, name="github_login"),
    path("github/login/callback/", views.github_callback, name="github_callback"),
    path(
        "github/login/finish/",
        views.GithubLogin.as_view(),
        name="github_login_todjango",
    ),
    path("kakao/login/", views.kakao_login, name="kakao_login"),
    path("kakao/login/callback/", views.kakao_callback, name="kakao_callback"),
    path(
        "kakao/login/finish/", views.KakaoLogin.as_view(), name="kakao_login_todjango"
    ),
    re_path(
        r"^account-confirm-email/$",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        views.ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
