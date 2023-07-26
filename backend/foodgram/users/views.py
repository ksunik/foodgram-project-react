from django.shortcuts import render
from rest_framework import status, viewsets
from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from .serializers import(CustomUserSerializer, ShowUserSerializer,
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


class ShowUserViewSet(UserViewSet):
# class ShowUserViewSet(viewsets.ModelViewSet)
    
    queryset = User.objects.all()
    serializer_class = ShowUserSerializer


    # def get_serializer_class(self):
    #     if self.action in ['subscriptions', 'subscribe']:
    #         return User
    # @action(detail=True, methods=['post', 'delete'])
    # def subscribe(self, request, pk):
    #     user = request.user
    #     author = def get_object_or_404(User, id=pk)
    #     if request.method == 'POST':
    #         serializer = SubscriptionSerializer(

    #         )
        