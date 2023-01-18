from rest_framework.permissions import BasePermission
from rest_framework import permissions

class IsAuthenticatedOrReadOnly(BasePermission):
	message = 'The user is not authenticated'

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		
		if request.META.get('user_id') is not None:
			return True
		return False
