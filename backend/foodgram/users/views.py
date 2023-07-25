from django.shortcuts import render
from rest_framework import status, viewsets
from django.contrib.auth import get_user_model
from .serializers import(CustomUserSerializer,
    PasswordSerializer)
    # ShowFollowerSerializer,
    # FollowerSerializer)

# Create your views here.
User = get_user_model()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [
    #     AllowAny,
    # ]
    # pagination_class = None
