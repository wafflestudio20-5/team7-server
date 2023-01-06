from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view()), #메인페이지, 트렌딩 정렬 기능 미구현
    path('write/', PostCreateView.as_view()), #새 글 작성
    path('@userid/<int:pk>', PostRetrieveDestroyView.as_view()), #특정 포스트 get,delete// @usernint:pk 말고 포스트 생성 시 작성한 url로 설정해야함
    path('write/id=<int:pk>', PostRetrieveUpdateView.as_view()),#특정 포스트 업데이트
]