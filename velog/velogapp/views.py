from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import *
from .permissions import IsCreatorOrReadOnly, IsCreator
from django.db.models import Q

class PostCreateView(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("data is not valid", status=status.HTTP_400_BAD_REQUEST)

class PostListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostListSerializer
    #lookup_field = 'author'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request):
        if request.path == '/':
            queryset = self.get_queryset().order_by('-like_count')
        elif request.path == '/recent':
            queryset = self.get_queryset().order_by('created_at')
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

class PostRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = PostDetailSerializer
    lookup_field = 'title'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(author=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)

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

# Create your views here.
