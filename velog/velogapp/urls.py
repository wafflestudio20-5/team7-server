from django.urls import include, path 
from django.conf.urls import url
from .views import CommentListCreateView, CommentDetailView

urlpatterns = [
    path('<int:pid>/comment/', CommentListCreateView.as_view()),
    path('<int:pid>/comment/<int:cid>', CommentUpdateDeleteView.as_view()),
]
