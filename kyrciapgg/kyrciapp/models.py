from django.contrib.auth.models import AbstractUser
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):
    region = models.CharField(max_length=100)

    class Meta:
        db_table = 'custom_user'