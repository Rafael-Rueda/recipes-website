from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class CommentManager(models.Manager):
    def get_by_id(self, id):
        return self.get(id=id)
class Comment(models.Model):
    objects = CommentManager()
    
    content = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)

    # Content Type - Polymorphism

    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content[:10]
    
class Tag(models.Model):
    tag = models.CharField(max_length=100)

    # Polymorphism

    content_type = models.ForeignKey(to=ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
