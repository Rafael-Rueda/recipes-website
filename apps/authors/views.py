from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ipware import get_client_ip

from apps.authors.forms import LoginForm, RecipeForm, RegisterForm
from apps.authors.models import UserLog
from apps.recipes import models
from utils.pagination import make_pagination


def register(request):
    form = RegisterForm(request.session.get('data_form'))

    if 'data_form' in request.session:
        del(request.session['data_form'])

    return render(request=request, template_name='authors/pages/register-page.html', context={'form': form})

def register_create(request):
    if (request.method != 'POST'):
        messages.error(request, 'Page not found.')
        return render(request=request, template_name='global/pages/404.html', status=404)

    request.session['data_form'] = request.POST
    modelform = RegisterForm(request.POST)

    if modelform.is_valid():
        
        user = modelform.save(commit=False)
        user.set_password(user.password)
        user.save()

        del(request.session['data_form'])
        messages.success(request, 'User created with success')

    return redirect('authors:register')

def login(request):
    form = LoginForm()
    if (request.method == 'POST'):
        form = LoginForm(request.POST)

        if (form.is_valid()):
            user = authenticate(
                request,
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                user_login(request, user)
                messages.success(request, 'User logged in with success.')
                return redirect('/')
            else:
                messages.error(request, 'Username or password invalid. Please try again.')
                return redirect('/login/')
    else:
        if request.user.is_authenticated:
            messages.info(request, f'You are already logged-in, {request.user.username}')
            return redirect('/')
        else:
            return render(request, 'authors/pages/login-page.html' , context={'form': form})
    
@login_required(login_url='authors:login', redirect_field_name='next')
def logout(request):
    if request.method != 'POST':
        messages.error(request, 'Page not found.')
        return render(request=request, template_name='global/pages/404.html', status=404)
    user_logout(request)
    messages.success(request, 'User logged-out with success.')
    return redirect('/login/')

@staff_member_required
def authors_admin(request):
    logs = UserLog.objects.all()
    recipes = models.Recipe.objects.order_by('-id')
    return render(request, 'authors/pages/admin-page.html', context={'logs': logs, 'recipes': recipes})

@staff_member_required
def authors_admin_save(request):
    if (request.method != 'POST'):
        messages.error(request, 'Page not found.')
        return render(request=request, template_name='global/pages/404.html', status=404)
    
    # Form data
    teste = request.POST
    is_published = request.POST.get('is_published', False) == 'on'
    preparation_steps_is_html = request.POST.get('preparation_steps_is_html', False) == 'on'
    recipe_id = request.POST.get('recipe', None)

    recipe = models.Recipe.objects.get(id=recipe_id)

    recipe.is_published = is_published
    recipe.preparation_steps_is_html = preparation_steps_is_html
    recipe.save()

    return redirect('authors:authors-admin')

@staff_member_required
def authors_admin_recipe(request, recipe_id):
    recipe = models.Recipe.objects.filter(id=recipe_id)
    title = recipe[0].title
    return render(request, 'recipes/pages/recipe-page.html', {"is_detail_page": True, 'recipes': recipe, 'title': title})
        


@receiver(user_logged_in)
def login_callback(sender, request, user, **kwargs):
    session_key = request.session.session_key
    user_ip = get_client_ip(request)[0]
    UserLog.objects.create(user=user, session_key=session_key, ip_address=user_ip)

@receiver(user_logged_out)
def logout_callback(sender, request, user, **kwargs):
    session_key = request.session.session_key
    userlogout = UserLog.objects.filter(user=user, logout_time=None, session_key=session_key).order_by('-login_time').first()
    if userlogout:
        userlogout.logout_time = timezone.now()
        userlogout.save()

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipe_selected = request.GET.get('recipe', '')
    form = ''
    create_allowed = False

    recipes = models.Recipe.objects.filter(author = request.user).order_by('-id')
    pages, page_obj = make_pagination(request, recipes, 7, 3)

    recipe_edit = None

    if request.session.get('createform') == True:
        if 'form_data' in request.session:
            form = RecipeForm(request.session.get('form_data'))
            del(request.session['form_data'])
        else:
            form = RecipeForm()
        del(request.session['createform'])
        
        create_allowed = True

    if request.method == 'GET' and recipe_selected:
        recipe_edit = models.Recipe.objects.get(id=recipe_selected) 
        if recipe_edit.author == request.user:
            form = RecipeForm(instance=recipe_edit)
        else:
            messages.error(request, 'Page not found.')
            return render(request=request, template_name='global/pages/404.html', status=404)
    

    return render(request, 'authors/pages/dashboard.html', {'recipes': page_obj, 'paginator': pages, 'other_parameters': f'&recipe={recipe_selected}', 'form': form, 'recipe_selected': recipe_selected, 'recipe_edit': recipe_edit, 'create_allowed': create_allowed})

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_update(request, recipe_id):
    if (request.method != 'POST'):
        messages.error(request, 'Page not found.')
        return render(request=request, template_name='global/pages/404.html', status=404)
    
    recipe_instance = get_object_or_404(models.Recipe, id=recipe_id)

    modelform = RecipeForm(request.POST, request.FILES, instance=recipe_instance)
    
    if modelform.is_valid():
        recipe = modelform.save(commit=False)
        recipe.is_published = False
        recipe.preparation_steps_is_html = False
        recipe.save()
        messages.success(request, 'Recipe updated with success.')

    return redirect('authors:dashboard')

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_create(request):
    request.session['createform'] = True
    if request.method == 'POST':
        modelform = RecipeForm(data=request.POST, files=request.FILES)

        request.session['form_data'] = request.POST

        if modelform.is_valid():
            data = modelform.save(commit=False)
            data.author = request.user
            data.is_published = False
            data.preparation_steps_is_html = False

            slug = slugify(data.title)
            if models.Recipe.objects.filter(slug=slug).exists():
                identifier = 1
                while models.Recipe.objects.filter(slug=f'{slug}-{identifier}').exists():
                    identifier += 1
                slug = f'{slug}-{identifier}'
    
            data.slug = slug
            
            data.save()

    return redirect('authors:dashboard')

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_delete(request, recipe_id):
    if request.method != 'POST':
        messages.error(request, 'Page not found.')
        return render(request=request, template_name='global/pages/404.html', status=404)

    models.Recipe.objects.filter(id = recipe_id).delete()

    return redirect('authors:dashboard')

