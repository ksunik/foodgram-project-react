from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .models import Recipe, Tag, Ingredient


# def get_page_paginator(request, queryset):
#     paginator = Paginator(queryset, 15)
#     page_number = request.GET.get('page')
#     return paginator.get_page(page_number)


# def index(request):
#     recipe = Recipe.objects.all()

#     recipe_obj = get_page_paginator(request, recipe)
#     context = {'recipe_obj': recipe_obj}
#     template =
