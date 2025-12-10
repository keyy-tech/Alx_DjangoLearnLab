from django.db import models
from django.contrib.auth.models import AbstractUser


class Accounts(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        default="profile_picture/default.jpg", upload_to="profile_picture",blank=True, null=True
    )
    followers = models.ManyToManyField(
        "self", related_name="following", symmetrical=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} {self.first_name or ''}"
