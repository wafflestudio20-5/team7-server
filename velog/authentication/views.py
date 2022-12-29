# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
# from drf_yasg.utils import swagger_auto_schema
# from . import serializers
# from rest_framework.response import Response
# from rest_framework.request import Request
# from rest_framework.views import APIView

#
# class SignupView(generics.GenericAPIView):
#
#     serializer_class = serializers.UserSerializer
#
#     @swagger_auto_schema(operation_summary="Create a user account")
#     def post(self, request):
#
#         data = request.data
#
#         serializer = self.serializer_class(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
#         return Response(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ProfileView(generics.GenericAPIView):
#     permission_classes = [IsAuthenticated]
#
#     serializer_class = serializers.UserSerializer
#
#     @swagger_auto_schema(operation_summary="Get a user profile")
#     def get(self, request: Request):
#
#         user = request.user
#
#         serializer = self.serializer_class(user, context={'request': request})
#
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
