from .models import Interaction
from rest_framework.serializers import ModelSerializer


class InteractionSerializer(ModelSerializer):

	class Meta:
		model = Interaction
		fields = '__all__'

	# Duplicate rows should not be created
	def create(self, validated_data):
		content = validated_data.get('content_id')
		user = validated_data.get('user_id')
		type = validated_data.get('type')

		interaction, _ = Interaction.objects.get_or_create(content_id=content, user_id=user, type=type)
		return interaction