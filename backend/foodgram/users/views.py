# from django.shortcuts import render
# from rest_framework import status, viewsets
# from djoser.views import UserViewSet
# from rest_framework.response import Response
# from django.contrib.auth import get_user_model
# from api.serializers import(CustomUserSerializer, ShowUserSerializer,
#     )

# User = get_user_model()


# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = CustomUserSerializer



# class ShowUserViewSet(UserViewSet):
# class ShowUserViewSet(viewsets.UserViewSet)
    
    # queryset = User.objects.all()
    # serializer_class = ShowUserSerializer

    # def me(self, request):
    #     serializer = self.get_serializer(request.user)
    #     return Response(serializer.data)


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
        