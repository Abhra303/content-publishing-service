from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsNotAuthenticated
from .serializers import UserSerializer, RegisterUserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class UserViewSet(ModelViewSet):
	serializer_class = UserSerializer
	queryset = User.objects.all()
	http_method_names = ('get', 'patch', 'delete')
	permission_classes = (IsAuthenticatedOrReadOnly, )


class RegisterNewUserView(CreateAPIView):
	serializer_class = RegisterUserSerializer
	permission_classes = (IsNotAuthenticated, )  # only annonymous user can register a new user

	def create(self, request, *args, **kwargs):
		try:
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer=serializer)
		except Exception as e:
			return Response({'error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)

		return Response({'message': 'user created succesfully'}, status=status.HTTP_201_CREATED)
