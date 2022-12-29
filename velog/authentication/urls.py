from dj_rest_auth.registration.urls import RegisterView
from dj_rest_auth.urls import LoginView, LogoutView, UserDetailsView
from django.urls import include, path

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("user/", UserDetailsView.as_view()),
    path("signup/", RegisterView.as_view()),
    # path('', include('dj_rest_auth.urls')),
    # path('signup/', include('dj_rest_auth.registration.urls')),
]
