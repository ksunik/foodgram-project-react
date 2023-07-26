"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views
# from rest_framework.routers import DefaultRouter
# from users.views import CustomUserViewSet

# router = DefaultRouter()
# router.register(r'users', CustomUserViewSet, basename='user')
urlpatterns = [
    # path('api/', include(router.urls)),
    path('api/', include('api.urls')),
    # path('api-token-auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
    # path('', include('recipes.urls')),

    # path('auth/', include('users.urls')),
    # path('auth/', include('django.contrib.auth.urls')),
]
