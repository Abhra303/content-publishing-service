from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookViewset, NewBookListView, TopBookListView


book_router = DefaultRouter()


'''
API endpoints for all the book related operations.
'''
urlpatterns = [
	path('new-contents/', NewBookListView.as_view(), name="books.new_contents"),
	path('top-contents/', TopBookListView.as_view(), name="books.top-contents"),
]

book_router.register(r"books", BookViewset, basename="books")
