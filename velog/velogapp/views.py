from rest_framework import generics, status, permissions
from rest_framework.response import Response
from velogapp.models import Post
from velogapp.serializers import *
from velogapp.permissions import IsCreatorOrReadOnly

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

class PostListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    # 특정 user가 쓴 글의 list만 가져오기

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    queryset = Post.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostDetailSerializer
        return PostSerializer

# Create your views here.
