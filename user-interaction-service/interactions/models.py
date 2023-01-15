from django.db import models

# Create your models here.

class Interaction(models.Model):
	READ_LIKE_CHOICES = (('R', 'Read'), ('L', 'Like'))
	user_id = models.PositiveIntegerField()
	content_id = models.PositiveIntegerField()
	type = models.CharField(max_length=2, choices=READ_LIKE_CHOICES)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return "user_id %d interaction"% (self.user_id)