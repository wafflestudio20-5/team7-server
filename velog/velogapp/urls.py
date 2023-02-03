from django.urls import path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', PostListView.as_view()), #메인페이지
    path('today/', PostListTodayView.as_view()),
    path('week/', PostListWeekView.as_view()),
    path('month/', PostListMonthView.as_view()),
    path('year/', PostListYearView.as_view()),
    path('recent/', PostListView.as_view()), #최신순으로 정렬
    path('lists/liked/', PostListView.as_view()), # 좋아요 한 포스트
    path('lists/read/', PostListView.as_view()), #최근 읽은 포스트
    path('search/', SearchListView.as_view()), # 포스트 검색 //ajax 적용?
    path('create_series/', SeriesCreateView.as_view()), # series 생성
    path('@<str:username>/', UserPostListView.as_view()), # 특정 user가 작성한 포스트 보기 // name->userid(username) 수정필요
    path('write/', PostCreateView.as_view()), #새 글 작성
    path('@<str:username>/series/', SeriesListView.as_view()), # 특정 user가 작성한 시리즈 목록 // name->userid(username) 수정필요
    path('@<str:username>/series/<str:url>', SeriesPostListView.as_view()), # 특정 user가 작성한 시리즈에 속해있는 포스트 조회,수정,삭제 // name->userid(username) 수정필요
    path('@<str:username>/tags/', UserTagListView.as_view()),  # 특정 user가 작성한 테그 목록 // name->userid(username) 수정필요
    path('@<str:username>/tags/<str:tag_name>', UserTagPostListView.as_view()), # 특정 user가 작성한 테그에 속해있는 포스트
    path('@<str:username>/<str:url>/', PostRetrieveDestroyView.as_view()), #특정 포스트 get,delete// name->userid(username) 수정필요
    path('write/id=<int:pid>/', PostRetrieveUpdateView.as_view()),#특정 포스트 update
    path('<int:pid>/comment/', CommentListCreateView.as_view()),
    path('<int:pid>/comment/<int:cid>', CommentUpdateDeleteView.as_view()),
    path('tags/', TagListView.as_view()), # tag 목록
    path('tags/<str:tag_name>', TagPostListView.as_view()), # 특정 tag가 포함된 포스트
    path('image_upload/<int:pid>', ImageCreateView.as_view()),
    path('image_delete/<int:pid>', ImageDeleteView.as_view()),
    path('image_list/<int:pid>', ImageListView.as_view()),
    # path('@<str:username>/series/<str:url>/<int:series_order>', SeriesPostView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
