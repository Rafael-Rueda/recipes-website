import os

from django.contrib import messages
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render

from apps.recipes import models
from utils.pagination import make_pagination

PER_PAGINATOR = os.environ.get('PER_PAGINATIOR', 7)
PER_PAGE = os.environ.get('PER_PAGE', 6)

def home(request):
    recipes = models.Recipe.objects.all().order_by('-id').filter(is_published=True)
    pages, page_obj = make_pagination(request, recipes, PER_PAGINATOR, PER_PAGE)

    if recipes:
        status_code = 200
    else:
        status_code = 404
        messages.error(request, 'There are no recipes here.')

    return render(request=request, template_name='recipes/pages/home.html', context={'recipes': page_obj, 'paginator': pages}, status=status_code)

def recipe(request, id):
    recipe = models.Recipe.objects.filter(id=id, is_published=True)
    
    if not recipe:
        text = ''
        messages.error(request, 'This recipe does not exist.')
        return render(request=request, template_name='global/pages/404.html', status=404, context={'text': text})
    
    title = recipe[0].title

    return render(request=request, template_name='recipes/pages/recipe-page.html', context={"is_detail_page": True, 'recipes': recipe, 'title': title})

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
