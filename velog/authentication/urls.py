# from allauth.account.views import login, logout, password_reset
from dj_rest_auth.registration.urls import RegisterView
from dj_rest_auth.urls import LoginView, LogoutView, UserDetailsView
from django.urls import include, path, re_path

urlpatterns = [
    path("login/", LoginView.as_view(), name="basic_login"),
    path("logout/", LogoutView.as_view(), name="basic_logout"),
    path("user/", UserDetailsView.as_view(), name="user_detail"),
    path("signup/", RegisterView.as_view(), name="basic_signup"),
    # path("password/reset/", password_reset),
    # path("social/login/", login),
    # path("social/logout/", logout),
]
