from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from .models import UserProfile
from .permissions import IsTheUserOrReadOnly
from .serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserProfileListSerializer,
    UserProfileDetailSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfileViewSet(
    viewsets.ModelViewSet,
):
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated, IsTheUserOrReadOnly)

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get("username")
        bio = self.request.query_params.get("bio")

        if username:
            queryset = queryset.filter(username__icontains=username)

        if bio:
            queryset = queryset.filter(bio__icontains=bio)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserProfileListSerializer

        return UserProfileDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
