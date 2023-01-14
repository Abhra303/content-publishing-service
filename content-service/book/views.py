from django.shortcuts import render
from django.db.models import Case, When
from rest_framework import viewsets, response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Book
from .serializers import BookSerializer
from content_service import internal_api
import requests
# Create your views here.

def get_author_id(request):
	'''
	NOTE: This function is TEMPORARY!

	Ideal case is to use a sdk for our product specifically
	to communicate between user service and other services.
	'''
	return request.user.id

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
		author_id = get_author_id(request)

		request.data['author_id'] = author_id
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
			book_ids = top_content_dict['book_ids']

			# use the order as given by the user_interaction top content api
			top_content = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(book_ids)])
			queryset = Book.objects.filter(pk__in=book_ids).order_by(top_content)
		except Exception:
			return None
		else:
			return queryset
