# from django.conf import settings
# from django.conf.urls.static import static
# from django.urls import include, path

# from . import views

# urlpatterns = [
#     path('', views.index),

#     # Страница со списком сортов мороженого:
#     # если получен запрос ice_cream/,
#     # будет вызвана функция ice_cream_list() из файла views.py
#     # path('ice_cream/', views.ice_cream_list),

#     # Отдельная страница с информацией о сорте мороженого
#     # если получен запрос ice_cream/<любой_набор_символов>,
#     # будет вызвана функция ice_cream_detail() из файла views.py
#     # path('ice_cream/<pk>/', views.ice_cream_detail),
# ]

# # Позволяет обращаться к файлам дирректории в MEDIA_ROOT
# # по имени, через префикс MEDIA_URL
# if settings.DEBUG:
#     urlpatterns += static(
#         settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
#     )

# from django.urls import path
# from . import views

# app_name = 'recipes'

# urlpatterns = [
    # path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    # path('recipe/', views.recipe_list, name='recipe_list'),
    # path('', views.index),

    # ]