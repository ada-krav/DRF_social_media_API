from django.contrib.auth import get_user_model
from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
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
            return UserProfileDetailSerializer

        return UserProfileListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=["GET"], detail=True, url_path="un-follow")
    def un_follow_user(self, request, pk=None):
        user = get_user_model().objects.get(id=request.user.id)
        other = get_user_model().objects.get(id=pk)
        if user != other:
            if user in other.profile.followers.all():
                with transaction.atomic():
                    other.profile.followers.remove(user.id)
                    user.profile.following.remove(other.id)
                    other.save()
                    user.save()
            else:
                with transaction.atomic():
                    other.profile.followers.add(user.id)
                    user.profile.following.add(other.id)
                    other.save()
                    user.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=str,
                description="Filter by username that contains specified symbol(s), "
                            "case insensitive (ex. ?username=oo)"

            ),
            OpenApiParameter(
                "bio",
                type=str,
                description="Filter by bio that contains specified symbol(s), "
                            "case insensitive (ex. ?bio=oo)"
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)