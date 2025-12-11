from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
# class Notification(models.Model):
#     recipient = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
#     actor = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
#     verb = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)