from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import *
from .permissions import IsCreatorOrReadOnly, IsCreator
from django.db.models import Q
from django.shortcuts import get_object_or_404
import re

class PostCreateView(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            author = request.user
            post = serializer.save(author=author)
            # create or get tag
            create_tag = request.data.get("create_tag")
            create_tag.replace("\n", ",")
            tag_regex = re.findall('([0-9a-zA-Z가-힣]*),', create_tag) # 쉼표 또는 엔터로 split 되도록 수정 필요
            tags_list = [Tag.objects.get_or_create(
                tag_name=t) for t in tag_regex]
            for tag, bool in tags_list:
                post.tags.add(tag.pk)
            post.save()
            # create or get series
            series = request.data.get("get_or_create_series") # post 작성 시 series 설정은  create_series로만 저장 가능
            if series != "":
                post.series = Series.objects.get_or_create(series_name=series, author=author)[0]
                post.save()
            else:
                pass
            serializer = PostSerializer(
                post,
                context={"request": request},
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request):
        if request.path == '/':
            queryset = self.get_queryset().order_by('-likes')
        elif request.path == '/recent/':
            queryset = self.get_queryset().order_by('-created_at')
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

class UserPostListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request, name):
        post = Post.objects.filter(author__name=name).order_by('-created_at')
        serializer = PostListSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)

class PostRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = PostDetailSerializer
    lookup_field1, lookup_field2 = 'name', 'title'


    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)


    def get(self, request, name, title):
        post = self.get_queryset().get(author__name=name, title=title)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    # post 요청 시 좋아요 추가/제거
    def post(self, request, name, title):
        post = self.get_queryset().get(author__name=name, title=title)
        user = request.user
        if post.like_user.filter(pk=request.user.pk).exists():
            post.like_user.remove(user)
            post.likes -= 1
            post.save()
        else:
            post.like_user.add(user)
            post.likes += 1
            post.save()
        return self.get(request, name, title)
    # 해당 post의 comment도 불러오도록 해야 함

class PostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCreator]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pid'

class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, pid, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        post = Post.objects.get(pid=pid)
        #get pid for post in comment

        if serializer.is_valid():
            author = request.user
            parent_comment = request.data.get("parent_comment", None)
            serializer.save(author=author, post=post)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(post=self.kwargs['pid'])
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'cid'

    def update(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs['cid'])
        is_updated = True
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(is_updated=is_updated)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TagListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    def get(self, request):
        queryset = self.get_queryset()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

class TagPostListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request, tag_name):
        post = Post.objects.filter(tags__tag_name=tag_name)
        serializer = PostListSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)

class SeriesListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    def get(self, request, name):
        series = Series.objects.filter(author__name=name)
        serializer = SeriesSerializer(series, many=True, context={'request': request})
        return Response(serializer.data)

class SeriesPostListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SeriesSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request, name, series_name):
        post = Post.objects.filter(author__name=name, series__series_name=series_name).order_by('-created_at')
        serializer = PostSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)


class SearchListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request):
        word = request.GET.get('q', None)
        if word:
            post = Post.objects.filter(Q(content__icontains=word) |
                                    Q(title__icontains=word)
                                   ).order_by('-likes')
            serializer = PostListSerializer(post, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response()


# Create your views here.
