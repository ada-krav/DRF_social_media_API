# Generated by Django 4.2 on 2023-04-23 19:36

from django.db import migrations, models
import social_media.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hashtag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=31, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=127)),
                ("text", models.CharField(max_length=511)),
                ("created_at", models.DateTimeField(auto_now=True)),
                (
                    "post_picture",
                    models.ImageField(
                        null=True, upload_to=social_media.models.post_picture_file_path
                    ),
                ),
                (
                    "hashtags",
                    models.ManyToManyField(
                        blank=True, related_name="posts", to="social_media.hashtag"
                    ),
                ),
            ],
        ),
    ]
