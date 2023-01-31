from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view()), #메인페이지
    path('recent/', PostListView.as_view()), #최신순으로 정렬
    path('lists/liked/', PostListView.as_view()), # 좋아요 한 포스트
    path('lists/read/', PostListView.as_view()), #최근 읽은 포스트
    path('search/', SearchListView.as_view()), # 포스트 검색 //ajax 적용?
    path('@<str:name>/', UserPostListView.as_view()), # 특정 user가 작성한 포스트 보기 // name->userid(username) 수정필요
    path('write/', PostCreateView.as_view()), #새 글 작성
    path('@<str:name>/series/', SeriesListView.as_view()), # 특정 user가 작성한 시리즈 목록 // name->userid(username) 수정필요
    path('@<str:name>/series/<str:series_name>', SeriesPostListView.as_view()), # 특정 user가 작성한 시리즈에 속해있는 포스트 // name->userid(username) 수정필요
    path('@<str:name>/<str:url>/', PostRetrieveDestroyView.as_view()), #특정 포스트 get,delete// name->userid(username) 수정필요
    path('write/id=<int:pid>/', PostRetrieveUpdateView.as_view()),#특정 포스트 update
    path('<int:pid>/comment/', CommentListCreateView.as_view()),
    path('<int:pid>/comment/<int:cid>', CommentUpdateDeleteView.as_view()),
    path('tags/', TagListView.as_view()), # tag 목록
    path('tags/<str:tag_name>', TagPostListView.as_view()), # 특정 tag가 포함된 포스트
]