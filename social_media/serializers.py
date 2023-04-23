from rest_framework import serializers

from social_media.models import Hashtag, Post


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("id", "name")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "title",
            "text",
            "created_at",
            "post_picture",
            "hashtags",
        )
        read_only_fields = ("id", "owner")


class PostListSerializer(PostSerializer):
    hashtags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
