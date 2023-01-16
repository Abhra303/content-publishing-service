from .views import ReadHandlerView, LikeHandlerView, TopContentView
from django.urls import path


urlpatterns = [
	path('read', ReadHandlerView.as_view(), name='interactions.read'),
	path('like', LikeHandlerView.as_view(), name='interactions.like'),
	path('contents/books/top-contents', TopContentView.as_view(), name='interactions.top_contents'),
]
