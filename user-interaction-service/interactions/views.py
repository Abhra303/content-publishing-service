from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Interaction
from django.db.models import Count
from rest_framework.views import APIView
from .serializers import InteractionSerializer
# Create your views here.

class ReadLikeHandler(CreateAPIView):
	'''
	Mixin class to handle read like events. This shouldn't
	directly handle API endpoints.
	Classes that inherit this class, must set the 'type'
	attribute. The accepted values are 'Read' and 'Like'.
	'''
	type = None

	def create(self, request, *args, **kwargs):
		if not self.type:
			raise Exception('type attribute must be set for the view')
		if self.type == 'Read':
			request.data['type'] = 'R'
		elif self.type == 'Like':
			request.data['type'] = 'L'
		else:
			raise Exception('type attribute has unrecognized value')

		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer=serializer)
		header = self.get_success_headers(serializer.data)
		
		# NEED-DISCUSSION: should this message be anyway returned if no
		# rows are created (i.e. in case of duplicate rows)
		return Response({'message': 'operation succesful'}, status=status.HTTP_201_CREATED, headers=header)

class ReadHandlerView(ReadLikeHandler):
	serializer_class = InteractionSerializer
	type = 'Read'


class LikeHandlerView(ReadLikeHandler):
	serializer_class = InteractionSerializer
	type = 'Like'


class TopContentView(APIView):
	'''
	This view is for internal API only. Response contains
	array of content_ids sorted in the order of most interactions.
	'''

	def get(self, request):
		queryset = Interaction.objects.values('content_id').annotate(count=Count('content_id'))
		sorted_queryset = queryset.order_by('-count')

		response_dict = {'content_ids': sorted_queryset.values_list('content_id', flat=True)}
		return Response(response_dict, status=status.HTTP_200_OK)
