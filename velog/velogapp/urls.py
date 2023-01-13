from django.urls import path

from .views import *

urlpatterns = [
    path("", PostListView.as_view()),  # 메인페이지
    path("recent/", PostListView.as_view()),  # 최신순으로 정렬
    # path('@<userid>/', PostListView.as_view()), # 특정 user가 작성한 글 보기
    path("write/", PostCreateView.as_view()),  # 새 글 작성
    path(
        "@<username>/<title>/", PostRetrieveDestroyView.as_view()
    ),  # 특정 포스트 get,delete// user의 field도 사용하도록 만들어야함, title 중복 문제
    path("write/id=<int:id>/", PostRetrieveUpdateView.as_view()),  # 특정 포스트 업데이트
]
