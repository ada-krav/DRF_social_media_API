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
    permission_classes = (IsAuthenticated, IsTheUserOrReadOnly,)
    pagination_class = PostPagination

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        favorite_people_list = self.request.user.profile.following.all()

        queryset = self.queryset.filter(
            owner__in=list(favorite_people_list) + [self.request.user.id]
        )

        hashtag = self.request.query_params.get("hashtags")

        if hashtag:
            queryset = queryset.filter(hashtags__name__icontains=hashtag)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
