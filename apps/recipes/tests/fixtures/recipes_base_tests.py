from django.contrib.auth.models import User
from django.test import TestCase

from apps.recipes import models


class RecipeMixin:
    def _make_category(self, name='Categoria'):
        return models.recipe_category.objects.create(name=name)

    def _make_user(
        self,
        username='User',
        password='123456',
        email='user@email.com',
        first_name='user',
        last_name='name',
    ):
        return User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

    # Usable
    def make_recipe(
        self,
        title='Test',
        description='test',
        slug='slug-test',
        preparation_time=2,
        preparation_time_unit='Minutos',
        servings=12,
        servings_unit='Pessoas',
        preparation_steps='test',
        preparation_steps_is_html=False,
        created_at='',
        updated_at='',
        is_published=True,
        category={},
        author={},
        cover='image/test/path',
    ):
        return models.Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            created_at=created_at,
            updated_at=updated_at,
            is_published=is_published,
            category=self._make_category(**category),
            author=self._make_user(**author),
            cover=cover,
        )

    
    def make_recipe_default(
        self,
        title='Test', 
        description= 'test',
        slug = 'slug-test',
        preparation_time = 2,
        preparation_time_unit = 'Minutos',
        servings = 12,
        servings_unit = 'Pessoas',
        preparation_steps = 'test',
        created_at = '',
        updated_at = '',
        category = {},
        author = {},
        cover = 'image/test/path',
    ):
        return models.Recipe.objects.create(
            title=title, 
            description= description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            created_at = created_at,
            updated_at = updated_at,
            category = self._make_category(**category),
            author = self._make_user(**author),
            cover = cover,
        )
    
    def make_recipes(self, len=12):
        recipes = []
        for c in range(len):
            kwargs = {
                'title': f'Test-{c}',
                'slug': f'slug-{c}', 
                'author': {'username': f'user_{c}'}, 
                'cover': ''}
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes

class TestBase(TestCase, RecipeMixin):
    # Test Fixtures
    ...