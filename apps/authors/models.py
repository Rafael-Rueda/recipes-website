from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from apps.comments.models import Comment


class UserLog(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return str(self.session_key)
    

class UserProfile(models.Model):
    author = models.OneToOneField(to=User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=900)
    comments = GenericRelation(Comment)

    def __str__(self):
        return f"Profile of {self.author.username}"
