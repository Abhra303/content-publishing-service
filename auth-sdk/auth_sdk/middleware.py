import requests
from django.conf import global_settings

class AuthMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		# Code to be executed for each request before
		# the view (and later middleware) are called.
		# TODO: 'token' should be mentioned in request
		# header. The 'url' should also be dynamic.

		url = '127.0.0.1:8000/users/verify-token/'
		token = request.data.get('token')

		if token:
			try:
				response = requests.post(url, {'token': token})
				if response.status_code == 200:
					re_dict = response.json()
					request.data['user_id'] = re_dict['user_id']
					
			except Exception as e:
				raise e

		response = self.get_response(request)

		return response