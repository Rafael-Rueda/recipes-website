# PARA CRIAR UM ARQUIVO SIGNALS.PY É NECESSÁRIO INICIALIZÁ-LO NO APPS.PY:
#    def ready(self):
#       import apps.recipes.signals

import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from apps.recipes.models import Recipe


def remove_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...

@receiver(pre_delete, sender=Recipe)
def pre_delete_a_recipe(sender, instance, *args, **kwargs):
    old_instance = Recipe.objects.get(pk=instance.pk)
    remove_cover(old_instance)

@receiver(pre_save, sender=Recipe)
def pre_save_a_recipe(sender, instance, *args, **kwargs):
    if instance.pk is not None:
        old_instance = Recipe.objects.get(pk=instance.pk)
        if instance.cover == old_instance.cover:
            ...
        else:
            remove_cover(old_instance)