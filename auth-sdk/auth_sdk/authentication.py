from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .settings import AUTH_SERVICE_URL
import requests

class UserAuthentication(BaseAuthentication):
	def authenticate(self, request):
		url = AUTH_SERVICE_URL + 'verify-token/'
		auth = request.META.get('HTTP_AUTHORIZATION', '').split()
		if not auth or auth[0].lower() != 'bearer':
			return None
		if len(auth) == 1:
			msg = 'Invalid Authorization header. No credentials provided.'
			raise exceptions.AuthenticationFailed(msg)
		elif len(auth) > 2:
			msg = 'Invalid Authorization header. Credentials string should not contain spaces.'
			raise exceptions.AuthenticationFailed(msg)
		token = auth[1]

		try:
			response = requests.post(url, {'token': token})
			print(response)
			if response.status_code == 200:
				re_dict = response.json()
				request.META['user_id'] = re_dict['user_id']
				return None
				
		except Exception as e:
			raise exceptions.AuthenticationFailed('Something went wrong while authenticating user')
			
		return None