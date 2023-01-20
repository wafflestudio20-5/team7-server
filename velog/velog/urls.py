"""velog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import ConfirmEmailView, EmailVerificationSentView
from allauth.socialaccount.views import connections
from dj_rest_auth.views import UserDetailsView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="velog API",
        default_version="v1",
        description="A REST API for a velog service",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@app.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(
        "swagger<format>.json|.yaml)",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/v1/docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/accounts/", include("dj_rest_auth.urls")),
    path("api/v1/accounts/", include("authentication.urls")),
    # path("api/v1/accounts/", include("allauth.urls")),
    # path("api/v1/accounts/", include("allauth.urls")),
    # path("accounts/", include("authentication.urls")),
    path("api/v1/", TemplateView.as_view(template_name="home.html"), name="home"),
    # 유효한 이메일이 유저에게 전달
    # re_path(
    #     r"^account-confirm-email/$",
    #     EmailVerificationSentView.as_view(),
    #     name="account_email_verification_sent",
    # ),
    # # 유저가 클릭한 이메일(=링크) 확인
    # re_path(
    #     r"^account-confirm-email/(?P<key>[-:\w]+)/$",
    #     ConfirmEmailView.as_view(),
    #     name="account_confirm_email",
    # ),
    path("api/v1/velog/", include("velogapp.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
