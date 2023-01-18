from django.db import models

# Create your models here.

class Book(models.Model):
	title = models.CharField(max_length=50, null=False)
	author = models.PositiveIntegerField()
	description = models.CharField(max_length=300, blank=True)
	story = models.TextField()
	published_date = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return "Book: " + self.title