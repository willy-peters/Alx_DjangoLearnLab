from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.decorators import action
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data.update({'token': token.key})
        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        user = validated['user']
        token = validated['token']
        data = UserSerializer(user, context={'request': request}).data
        data.update({'token': token})
        return Response(data)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        """
        Follow user with id=user_id
        """
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target)
        return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        """
        Unfollow user with id=user_id
        """
        target = get_object_or_404(User, id=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target)
        return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)