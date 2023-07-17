from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import RedirectView

from apps.comments.models import Comment
from apps.recipes.models import Recipe


def edit_comment(request, id):
    if request.method == 'POST':
        request.session['comment-form'] = {'content': request.POST.get('content'), 'id': id}
        last_page = request.META.get('HTTP_REFERER')
        return redirect(last_page)
    else:
        raise Http404()

def save_comment(request, id):
    if request.method == 'POST':
        comment = Comment.objects.get_by_id(id)
        comment.content = request.POST.get('content')
        comment.save()

        last_page = request.META.get('HTTP_REFERER')
        return redirect(last_page)
    else:
        raise Http404()
    
def delete_comment(request, id):
    if request.method == 'POST':
        comment = Comment.objects.get_by_id(id)
        comment.delete()

        last_page = request.META.get('HTTP_REFERER')
        return redirect(last_page)
    else:
        raise Http404()
    
class create_comment_recipe(RedirectView):
    def post(self, request, id, *args, **kwargs):
        recipe_content_type = ContentType.objects.get_for_model(Recipe)
        if request.POST.get('content'):
            Comment.objects.create(content=request.POST.get('content'), author=request.user, content_type=recipe_content_type, object_id=id)
        last_page = request.META.get('HTTP_REFERER')
        return redirect(last_page)