import os

from django.contrib import messages
from django.db.models import F, Q, Value
# EX: model.objects.filter( Q(id = F('author__id')) | Q(id = 1) ).annotate(full_name=Value('name'))
from django.db.models.aggregates import Count, Max, Min, Sum
# EX: model.objects.aggregate(Count('id')) >> {'id__count': 100}
from django.db.models.functions import Concat
# EX: model.objects.all().annotate(full_name=Concat(F('author__first_name'), Value(' Silva')))
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView

from apps.recipes import models
from utils.pagination import make_pagination

PER_PAGINATOR = os.environ.get('PER_PAGINATIOR', 7)
PER_PAGE = os.environ.get('PER_PAGE', 6)

def home(request):
    recipes = models.Recipe.objects.get_published().select_related('author', 'category')
    pages, page_obj = make_pagination(request, recipes, PER_PAGINATOR, PER_PAGE)

    if recipes:
        status_code = 200
    else:
        status_code = 404
        messages.error(request, 'There are no recipes here.')

    return render(request=request, template_name='recipes/pages/home.html', context={'recipes': page_obj, 'paginator': pages}, status=status_code)

class homeCBV(ListView):
    model = models.Recipe
    context_object_name = 'recipes'
    # ordering = '-id'
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.order_by('-id').filter(is_published=True)
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        pages, page_obj = make_pagination(self.request, ctx.get('recipes'), PER_PAGINATOR, PER_PAGE)
        ctx['recipes'] = page_obj
        ctx['paginator'] = pages
        return ctx
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset(*args, **kwargs)
        if self.object_list:
            status_code = 200
        else:
            status_code = 404
            messages.error(request, 'There are no recipes here.')
            return render(request=request, template_name='recipes/pages/home.html', status=status_code) 
        context = self.get_context_data()
        return self.render_to_response(context)

def recipe(request, id):
    recipe = models.Recipe.objects.filter(id=id, is_published=True)

    comment_form = request.session.get('comment-form', '')
    
    if request.session.get('comment-form'):
        del(request.session['comment-form'])
    
    if not recipe:
        text = ''
        messages.error(request, 'This recipe does not exist.')
        return render(request=request, template_name='global/pages/404.html', status=404, context={'text': text})
    
    title = recipe[0].title

    return render(request=request, template_name='recipes/pages/recipe-page.html', context={"is_detail_page": True, 'recipes': recipe, 'title': title, 'comment_form': comment_form})

def category(request, category_id):
    recipes = models.Recipe.objects.order_by('-id').filter(category__id=category_id, is_published=True)

    try:
        models.recipe_category.objects.get(id=category_id)
    except models.recipe_category.DoesNotExist:
        text = ''
        messages.error(request, 'This category does not exist.')
        return render(request=request, template_name='global/pages/404.html', status=404, context={'text': text})
    
    pages, page_obj = make_pagination(request, recipes, PER_PAGINATOR, PER_PAGE)

    title = models.recipe_category.objects.get(id=category_id).name

    return render(request=request, template_name='recipes/pages/category.html', context={'recipes': page_obj, 'title': title, 'paginator': pages})

def search(request):
    search = request.GET.get('q', '').strip()

    recipes = models.Recipe.objects.filter(
        ~Q(is_published=False) &
        Q(is_published=True) &
        Q(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
        ).order_by('-id')
    
    if recipes:
        status_code = 200
    else:
        status_code = 404
        messages.error(request, 'This recipe does not exist.')
    
    if not search:
        if request.META.get('HTTP_REFERER', None) is not None:
            return redirect(request.META.get('HTTP_REFERER', None))
        else:
            text = ''
            messages.error(request, 'Search not found. Please type something valid in the search field.')
            return render(request=request, template_name='global/pages/404.html', status=404, context={'text': text})
        
    pages, page_obj = make_pagination(request, recipes, PER_PAGINATOR, PER_PAGE)
    
    return render(request=request, template_name='recipes/pages/search.html', status=status_code, context={'title': search, 'search_term': search, 'recipes': page_obj, 'paginator': pages, 'other_parameters': f'&q={search}'})

# API

def normalize_dict_recipes(request, dict_recipes):
    for dict_recipe in dict_recipes:
        dict_recipe['cover'] = request.build_absolute_uri('/') + dict_recipe['cover'].url[1:]
        del dict_recipe['is_published']
        del dict_recipe['preparation_steps_is_html']
        dict_recipe['created_at'] = str(models.Recipe.objects.get(id=dict_recipe['id']).created_at)
        dict_recipe['updated_at'] = str(models.Recipe.objects.get(id=dict_recipe['id']).updated_at)

def recipesAPIv1(request):
    dict_recipes = [model_to_dict(_recipe) for _recipe in models.Recipe.objects.all().select_related('author', 'category')]

    normalize_dict_recipes(request, dict_recipes)

    return JsonResponse(
        dict_recipes,
        safe=False
    )

def recipeAPIv1(request, id):
    dict_recipes = [model_to_dict(models.Recipe.objects.get(id=id))]

    normalize_dict_recipes(request, dict_recipes) 

    return JsonResponse(
        dict_recipes,
        safe=False
    )
