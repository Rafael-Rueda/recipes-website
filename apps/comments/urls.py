from django.urls import path

from apps.comments import views

app_name = 'comments'

urlpatterns = [
    path('editcomment/<int:id>', view=views.edit_comment, name='edit_comment'),   
    path('savecomment/<int:id>', view=views.save_comment, name='save_comment'),
    path('deletecomment/<int:id>', view=views.delete_comment, name='delete_comment'),
    path('createcommentrecipe/<int:id>', view=views.create_comment_recipe.as_view(), name='create_comment'),
]
