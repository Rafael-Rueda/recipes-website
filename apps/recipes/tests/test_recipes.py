from unittest.mock import Mock, patch

from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import resolve, reverse
from parameterized import parameterized

from apps.recipes import models, views
from apps.recipes.tests.fixtures.recipes_base_tests import TestBase
from utils.pagination import make_pagination_range

# Test Driven Development
# Red / Green / Refactor

class URLsTest(TestCase):
    def test_recipes_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')

    def test_recipes_category_url_exists(self):
        expected_url = f'/recipes/category/1'
        category_url = reverse('recipes:category', kwargs={'category_id': 1})
        self.assertEqual(category_url, expected_url)

    def test_recipes_recipe_url_is_correct(self):
        recipe_url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(recipe_url, '/recipes/1')

    def test_recipes_search_url_is_correct(self):
        search_url = reverse('recipes:search')
        self.assertEqual(search_url, '/recipes/search')

class ViewsTest(TestBase):
    def test_recipes_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home')).func
        self.assertIs(view, views.home)
    
    def test_recipes_recipe_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1})).func
        self.assertIs(view, views.recipe)

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1})).func
        self.assertIs(view, views.category)

    def test_recipes_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search')).func
        self.assertIs(view, views.search)

    def test_recipes_search_is_escaped(self):
        text = '<script> Test <script>'
        expected_text = '&lt;script&gt; Test &lt;script&gt;'
        response = self.client.get(reverse('recipes:search') + f'?q={text}')
        self.assertIn(expected_text, response.content.decode('utf-8'))

    def test_recipes_search_view_is_filtering_correctly(self):
        # Need a recipe for check
        recipe = self.make_recipe()
        
        text = 'test'
        response = self.client.get(reverse('recipes:search') + f'?q={text}')
        context = response.context['recipes']
        self.assertIn(recipe, context)

class TemplatesTest(TestBase):

    def test_recipes_home_view_points_to_correct_template(self):
        # Need a recipe for check
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_recipe_view_points_to_correct_template(self):
        # Need a recipe for check
        self.make_recipe()

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/pages/recipe-page.html')

    def test_recipes_category_view_points_to_correct_template(self):
        # Need a recipe for check
        self.make_recipe()

        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_recipes_search_view_point_to_correct_template(self):
        # Need a recipe for check
        self.make_recipe()

        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    # No content (404)

    def test_recipes_home_view_has_no_content_by_default(self):
        response = self.client.get(reverse('recipes:home'))
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 404)
        # self.assertIn('<h2 class="text-404">', response.content.decode('utf-8'))
        self.assertEqual(messages[0].level_tag == 'message-error', True)

    def test_recipes_recipe_view_points_to_404_by_default(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'global/pages/404.html')
    
    def test_recipes_category_view_points_to_404_by_default(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'global/pages/404.html')

    def test_recipes_search_view_points_to_404_if_no_search(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'global/pages/404.html')

class ContextsTest(TestBase):
    def test_recipes_home_view_context_is_correct(self):
        # Need a recipe for check
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        context = response.context['recipes']
        self.assertEqual(context.object_list[0], models.Recipe.objects.get(id=1))

    def test_recipes_recipe_view_context_is_correct(self):
        # Need a recipe for check
        self.make_recipe()

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        context = [response.context['recipes'],
                   response.context['is_detail_page'],
                   ]
        self.assertEqual(context[0].first(), models.Recipe.objects.get(id=1))
        self.assertEqual(context[1], True)

    def test_recipes_category_view_context_is_correct(self):
        # Need a recipe for check
        self.make_recipe()

        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        context = response.context['recipes']
        self.assertEqual(context.object_list[0], models.Recipe.objects.get(id=1))

    def test_recipes_search_view_context_is_correct(self):
        # Need a recipe for check
        self.make_recipe()

        search = 'Test'
        response = self.client.get(reverse('recipes:search') + '?q=' + search + '&page=1')
        context = [response.context['title'],
                   response.context['search_term'],
                   response.context['recipes'],
                   response.context['paginator'],
                   response.context['other_parameters'],
                   ]

        self.assertEqual(context[0], search)
        self.assertEqual(context[1], search)
        self.assertEqual(context[2][0], models.Recipe.objects.get(title=search))
        self.assertEqual(context[3], make_pagination_range(1,1,1))
        self.assertEqual(context[4], f'&q={search}')

class ModelsTest(TestBase):

    # Recipe Model

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])

    def test_recipes_model_Recipe_fields_raise_error_when_exceeds_max_length(self, field, max_length):
        # Need a recipe for check
        recipe = self.make_recipe()

        setattr(recipe, field, 'C' * (max_length + 1))
        with self.assertRaises(ValidationError):
            recipe.full_clean()
    
    def test_recipes_model_Recipe_is_published_is_false_by_default(self):
        # Need a recipe for check
        recipe = self.make_recipe_default()

        self.assertFalse(recipe.is_published, msg='!!! Recipe is_published is True by default !!!')

    def test_recipes_model_Recipe_preparation_steps_is_html_is_false_by_default(self):
        # Need a recipe for check
        recipe = self.make_recipe_default()

        self.assertFalse(recipe.preparation_steps_is_html, msg='!!! Recipe preparation_steps_is_html is True by default !!!')

    def test_recipes_model_Recipe_string_representation(self):
        # Need a recipe for check
        recipe = self.make_recipe()

        self.assertEqual(str(recipe), recipe.title)

    # Category Model

    @parameterized.expand([
        ('name', 65),
    ])

    def test_recipes_model_Category_fields_raise_error_when_exceeds_max_length(self, field, max_length):
        # Need a category for check
        category = self._make_category()

        setattr(category, field, 'C' * (max_length + 1))
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_recipes_model_Category_string_representation(self):
        # Need a category for check
        category = self._make_category()

        category.name = 'Categoria'
        self.assertEqual(str(category), category.name)

class PaginationTest(TestBase):
    def test_if_pagination_is_working(self):
        # Need a recipe for check
        self.make_recipe()
        self.make_recipe(slug= 'slug-test2', author={'username': 'teste'})

        with patch('apps.recipes.views.PER_PAGE', new=1):
            response = self.client.get(reverse('recipes:home'))
            context = response.context['recipes']
            paginator = context.paginator

            self.assertEqual(paginator.num_pages, 2)
            self.assertEqual(len(paginator.get_page(1)), 1)

# class AdminTest(TestBase):
#     def test_if_admin_page_is_working(self):
#         # Need a user for check
#         user = self._make_user()

#         user.is_staff = True
#         user.is_superuser = True

#         user.save()

#         self.client.login(username=user.username, password=user.password)
#         response = self.client.get(reverse('admin:index'))
#         self.assertEqual(response.status_code, 200)