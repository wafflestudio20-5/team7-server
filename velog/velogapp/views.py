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
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(created_by=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)
    def get(self, request):
        queryset = self.get_queryset()
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

class PostRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = PostDetailSerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(created_by=self.request.user) |
                                       Q(is_private=False)
                                       )
        else:
            return Post.objects.filter(is_private=False)

class PostRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsCreator]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Create your views here.
