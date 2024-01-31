from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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
        
    followed_users = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def follow_user(self, user_to_follow):
        self.followed_users.add(user_to_follow)

    def unfollow_user(self, user_to_unfollow):
        self.followed_users.remove(user_to_unfollow)

    def is_following(self, user):
        return self.followed_users.filter(id=user.id).exists()
    
class FollowedSummoner(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)

    def __str__(self):
        return self.name