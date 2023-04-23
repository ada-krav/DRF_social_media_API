from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from social_media.models import Hashtag, Post
from social_media.permissions import IsTheUserOrReadOnly
from social_media.serializers import (
    HashtagSerializer,
    PostListSerializer,
    PostSerializer,
)


class HashtagViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Hashtag.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = HashtagSerializer


class PostPagination(PageNumberPagination):
    page_size = 11
    max_page_size = 101


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related("hashtags")
    permission_classes = (
        IsAuthenticated,
        IsTheUserOrReadOnly,
    )
    pagination_class = PostPagination

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        following_list = self.request.user.profile.following.all()

        queryset = self.queryset.filter(
            owner__in=list(following_list) + [self.request.user.id]
        )

        hashtag = self.request.query_params.get("hashtag")
        hashtags = self.request.query_params.get("hashtags")

        if hashtag:
            queryset = queryset.filter(hashtags__name__icontains=hashtag)

        if hashtags:
            hashtags_ids = self._params_to_ints(hashtags)
            queryset = queryset.filter(hashtags__id__in=hashtags_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtag",
                type=str,
                description="Filter by hashtag that contains specified symbol(s), "
                "case insensitive (ex. ?hashtag=oo)",
            ),
            OpenApiParameter(
                "hashtags",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by hashtags id (ex. ?hashtags=2,5)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
