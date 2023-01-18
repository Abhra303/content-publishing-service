from django.core.management import call_command
from django.db.models import Case, When
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.generics import ListAPIView
from auth_sdk.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer
from content_service import internal_api
import requests
# Create your views here.

class BookViewset(viewsets.ModelViewSet):
	'''
	CRUD API handler for book content service. This Viewset
	takes care of alll the get requests, post requests,
	put/patch requests and delete requests.
	The API endpoints can be seen in ./urls.py
	'''
	serializer_class = BookSerializer
	queryset = Book.objects.all()
	permission_classes = (IsAuthenticatedOrReadOnly, )

	def create(self, request, *args, **kwargs):
		'''
		create() should automatically put the author_id of
		the current user. This method should only work for
		authenticated users.
		TODO: For now we are using django's inbuilt user model.
		This should not be the case as we are creating a seperate
		user micro-service.
		'''
		request.data['author_id'] = request.META.get('user_id')
		return super().create(request, *args, **kwargs)


class NewBookListView(ListAPIView):
	serializer_class = BookSerializer
	queryset = Book.objects.order_by('-published_date')


class TopBookListView(ListAPIView):
	'''
	This content API handler return response containing a
	list of books sorted in the order of most interactions
	(reads and likes)
	'''
	serializer_class = BookSerializer

	def get_queryset(self):
		try:
			response_data = requests.get(internal_api.USER_INTERACTION_TOP_CONTENTS_API)
			if response_data.status_code == 404:
				return None
			top_content_dict = response_data.json()
			book_ids = top_content_dict['content_ids']

			# use the order as given by the user_interaction top content api
			top_content = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(book_ids)])
			queryset = Book.objects.filter(pk__in=book_ids).order_by(top_content)
		except Exception:
			return None
		else:
			return queryset


@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def test_csv_upload_view(request):
	'''
	As this view is for testing purpose only, we need to
	make a seperate endpoint for testing. (maybe?)
	'''
	request.upload_handlers.pop(0)
	csv_file = request.data.get('csv_file')
	csv_file_path = csv_file.temporary_file_path()

	try:
		# use the 'upload_csv' command to process further
		call_command('upload_csv', csv_file_path)
	except Exception:
		return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	return Response(status=status.HTTP_201_CREATED)
