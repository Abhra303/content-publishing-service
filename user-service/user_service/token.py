from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.tokens import UntypedToken


# Response data containing only validation info is
# not enough. Micro-services need additional info like
# user_id, token_expiry for caching.
class UserTokenVerifySerializer(TokenVerifySerializer):
	def validate(self, attrs):
		data = super().validate(attrs)

		print(attrs)

		token = UntypedToken(attrs['token'])
		# token_expiry = self.context['token'].exp

		data.update({'user_id': token.payload['user_id'], 'valid': True, 'token_expiry': token.payload['exp']})

		return data


class UserTokenVerifyView(TokenVerifyView):
	serializer_class = UserTokenVerifySerializer
