from allauth.account.views import ConfirmEmailView
from authentication import views
from dj_rest_auth.registration.views import (RegisterView,
                                             ResendEmailVerificationView,
                                             VerifyEmailView)
from dj_rest_auth.urls import (PasswordResetConfirmView, PasswordResetView,
                               UserDetailsView)
from django.urls import path, re_path

urlpatterns = [
    path("user/", UserDetailsView.as_view(), name="user_detail"),
    path("signup/", RegisterView.as_view(), name="basic_signup"),
    path(
        "signup/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<uid>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view()),
    path("kakao/login/", views.kakao_login, name="kakao_login"),
    path("kakao/login/callback/", views.kakao_callback, name="kakao_callback"),
    path(
        "kakao/login/finish/", views.KakaoLogin.as_view(), name="kakao_login_todjango"
    ),
    path("github/login/", views.github_login, name="github_login"),
    path("github/login/callback/", views.github_callback, name="github_callback"),
    path(
        "github/login/finish/",
        views.GithubLogin.as_view(),
        name="github_login_todjango",
    ),
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
    re_path(
        r"^account-confirm-email/$",
        VerifyEmailView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^account-confirm-email/(?P<key>[-:\w]+)/$",
        ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
]
