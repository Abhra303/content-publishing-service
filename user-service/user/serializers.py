from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		exclude = ('password',)


class RegisterUserSerializer(ModelSerializer):
	
	class Meta:
		model = User
		fields = '__all__'
		read_only_fields = ('id', 'is_verified', 'is_active')
		write_only_fields = ('password')

	def create(self, validated_data):
		password = validated_data.pop("password", None)
		obj = self.Meta.model(**validated_data)
		if password is not None:
			obj.set_password(password)
		obj.save()
		return obj
