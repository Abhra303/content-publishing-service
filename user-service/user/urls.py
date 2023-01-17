from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import UserViewSet, RegisterNewUserView

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user.users')

urlpatterns = [
	path('users/create', RegisterNewUserView.as_view(), name='user.create_users'),
]

