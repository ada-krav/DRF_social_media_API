import os
import uuid

from django.db import models
from django.utils.text import slugify

from config import settings


class Hashtag(models.Model):
    name = models.CharField(max_length=31, unique=True)

    def __str__(self):
        return self.name


def post_picture_file_path(post, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(post.id)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "posts_pictures", filename)


class Post(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=127)
    text = models.CharField(max_length=511)
    created_at = models.DateTimeField(auto_now=True)
    post_picture = models.ImageField(null=True, upload_to=post_picture_file_path)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name="posts")

    def __str__(self):
        return self.title
