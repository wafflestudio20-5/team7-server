from django.urls import path
from .views import *

urlpatterns = [
    path('write/', PostCreateView.as_view()),
    path('@username/', PostListView.as_view()), #user의 이름에 따라 url이 달라짐
    path('@username/<int:pk>', PostRetrieveUpdateDestroyView.as_view()),
]