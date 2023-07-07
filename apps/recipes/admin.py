from django.contrib import admin

from . import models


class recipe_categoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(model_or_iterable=models.recipe_category, admin_class=recipe_categoryAdmin)

class RecipeAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ('id', 'title', 'slug', 'is_published')
    list_display_links = ('title',)
    list_editable = ('slug', 'is_published')

admin.site.register(models.Recipe, RecipeAdmin)
