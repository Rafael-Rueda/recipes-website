from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models

from apps.comments.models import Comment, Tag


class recipe_category(models.Model):
    name = models.CharField(max_length=65)
    
    def __str__(self):
        return self.name

class RecipeManager(models.Manager):
    def get_published(self): # self é sempre um ".objects" no Manager.
        return self.filter(is_published = True).order_by('-id')
class Recipe(models.Model):
    objects = RecipeManager() # Necessário instancia-lo em "objects" para linkar o Manager com o model.

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')
    category = models.ForeignKey(to=recipe_category, on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    comments = GenericRelation(Comment)
    tags = GenericRelation(Tag)

    def __str__(self):
        return self.title
    
    # Model validation

    # def clean(self, *args, **kwargs):
    #     if not self.pk and Recipe.objects.filter(title__iexact=self.title).exists():
    #         raise ValidationError({'title': 'A recipe with that title already exists.'})
