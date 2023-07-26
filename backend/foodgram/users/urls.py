# Импортируем из приложения django.contrib.auth нужный view-класс
# from django.contrib.auth.views import LogoutView 
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet


router = DefaultRouter()
router.register("users", CustomUserViewSet)
# app_name = 'users'

urlpatterns = [
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
    # path(
    #   'logout/',
    #   # Прямо в описании обработчика укажем шаблон, 
    #   # который должен применяться для отображения возвращаемой страницы.
    #   # Да, во view-классах так можно! Как их не полюбить.
    #   LogoutView.as_view(template_name='users/logged_out.html'),
    #   name='logout'
    # ),
]
