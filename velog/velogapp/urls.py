from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view()), #메인페이지
    path('recent/', PostListView.as_view()), #최신순으로 정렬
    path('@<str:name>/', UserPostListView.as_view()), # 특정 user가 작성한 글 보기
    path('write/', PostCreateView.as_view()), #새 글 작성
    path('@<str:name>/series/', SeriesListView.as_view()),
    path('@<str:name>/<title>/', PostRetrieveDestroyView.as_view()), #특정 포스트 get,delete// userid(username) field도 사용하도록 만들어야함, 중복 게시물 해결 필요
    path('write/id=<int:pid>/', PostRetrieveUpdateView.as_view()),#특정 포스트 업데이트
    path('<int:pid>/comment/', CommentListCreateView.as_view()),
    path('<int:pid>/comment/<int:cid>', CommentUpdateDeleteView.as_view()),
    path('tags/', TagListView.as_view()),
    path('tags/<str:tag_name>', TagPostListView.as_view()),
]