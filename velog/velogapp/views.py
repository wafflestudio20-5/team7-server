from django.shortcuts import render
from rest_framework import authentication
from rest_framework import generics
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import views
from .models import Post, Comment  
from .serializers import CommentSerializer
# Create your views here.

class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        created_by = request.user
        serializer = CommentSerializer(data=request.data)
        post = Post.objects.get("pid")
        #get pid for post in comment
        parent_comment = request.data.get("parent_comment")

        if serializer.is_valid():
            created_by = request.user
            parent_comment = request.data.get("parent_comment", None)
            serializer.save(
                created_by=created_by,
                post=post,
                parent_comment=parent_comment
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Comment.objects.filter(post=self.kwargs['pid'])

class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly, )
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

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