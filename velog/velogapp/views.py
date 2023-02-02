from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import *
from .permissions import IsCreatorOrReadOnly, IsCreator
from .paginations import PostListPagination
from django.db.models import Q
import re

class PostCreateView(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # url custom
            posturl = request.data.get("url")
            if posturl:
                pass
            else:
                posturl = request.data.get("title")
            while Post.objects.filter(url=posturl).exists():
                postid = Post.objects.filter(url=posturl).count()
                posturl += "-"+str(postid)
            author = request.user
            post = serializer.save(author=author, url=posturl)
            # create or get tag
            create_tag = request.data.get("create_tag")
            create_tag.replace("\n", ",")
            tag_regex = re.findall('([0-9a-zA-Z가-힣]*),', create_tag)
            tags_list = [Tag.objects.get_or_create(
                            tag_name=t, author=author)
                         for t in tag_regex]
            for tag, bool in tags_list:
                post.tags.add(tag.pk)
            post.save()
            # get series
            serializer = PostSerializer(
                post,
                context={"request": request},
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SeriesCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Series.objects.all()
    serializer_class = SeriesCreateSerializer
    def get(self, request):
        queryset = self.get_queryset().filter(author=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # create series
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # series url custom
            seriesurl = request.data.get("url")
            if seriesurl:
                pass
            else:
                seriesurl = request.data.get("series_name")
            serializer.save(author=request.user, url=seriesurl)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    pagination_class = PostListPagination
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request):
        if request.path == '/api/v1/velog/':
             queryset = self.get_queryset().order_by('-likes')
        elif request.path == '/api/v1/velog/recent/':
            queryset = self.get_queryset().order_by('-created_at')
        elif request.path == '/api/v1/velog/lists/liked/':
            if request.user.is_authenticated:
                queryset = self.get_queryset().filter(like_user=request.user)[::-1]
        elif request.path == '/api/v1/velog/lists/read/':
            if request.user.is_authenticated:
                queryset = self.get_queryset().filter(view_user=request.user)[::-1]
        serializer = PostListSerializer(queryset, many=True)
        return self.get_paginated_response(self.paginate_queryset(serializer.data))

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
    def get(self, request, username):
        post = Post.objects.filter(author__username=username).order_by('-created_at')
        serializer = PostListSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)

class PostRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = PostDetailSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request, username, url):
        post = self.get_queryset().get(author__username=username, url=url)
        # 조회한(GET 요청한) user 기록
        if request.user.is_authenticated:
            if post.view_user.filter(pk=request.user.pk).exists():
                post.view_user.remove(request.user)
                post.view_user.add(request.user)
            else:
                post.view_user.add(request.user)
        serializer = PostDetailSerializer(post, context={'request': request})
        return Response(serializer.data)
    # post 요청 시 좋아요 추가/제거
    def post(self, request, username, url):
        post = self.get_queryset().get(author__username=username, url=url)
        if request.user.is_authenticated:
            user = request.user
            if post.like_user.filter(pk=request.user.pk).exists():
                post.like_user.remove(user)
                post.likes -= 1
                post.save()
            else:
                post.like_user.add(user)
                post.likes += 1
                post.save()
            return self.get(request, username, url)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, username, url):
        post = self.get_queryset().get(author__username=username, url=url)
        self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)
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
    serializer_class = TagCountSerializer

    def get(self, request):
        queryset = Tag.objects.values('tag_name').distinct() # 현재에는 tag_name이 같으나 author가 달라질 수 있기에 중복제거
        serializer = TagCountSerializer(queryset, many=True) # TagCountSerializer로 적용
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

class UserTagListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    def get(self, request, username):
        tags = Tag.objects.filter(author__username=username)
        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)

class UserTagPostListView(generics.GenericAPIView): # PUT, DELETE 추가 필요(permission classes = [IsCreatorOrReadOnly]
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request, username, tag_name):
        post = Post.objects.filter(author__username=username, tags__tag_name=tag_name)
        serializer = PostListSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)

class SeriesListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    def get(self, request, username):
        series = Series.objects.filter(author__username=username)
        serializer = SeriesSerializer(series, many=True, context={'request': request})
        return Response(serializer.data)

class SeriesPostListView(generics.GenericAPIView): # PUT, DELETE 추가 필요(permission classes = [IsCreatorOrReadOnly]
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request, username, series_name):
        post = Post.objects.filter(author__username=username, series__series_name=series_name).order_by('-created_at')
        serializer = PostListSerializer(post, many=True, context={'request': request})
        return Response(serializer.data)


class SearchListView(generics.GenericAPIView): # ajax
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    pagination_class = PostListPagination
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
            return self.get_paginated_response(self.paginate_queryset(serializer.data))
        else:
            return Response()


# Create your views here.
