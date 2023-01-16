from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator


class TheUserManager(BaseUserManager):
	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('Email is required to create the user instance')
		email = self.normalize_email(email)
		user = self.model(email_id=email, **extra_fields)
		user.set_password(password)
		user.save(using=self.db)
		return user


class User(AbstractBaseUser):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email_id = models.EmailField(unique=True)
	phone_regex = RegexValidator(
		regex=r"^\+?1?\d{9,15}$",
		message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
	)
	phone_no = models.CharField(validators=[phone_regex], max_length=17, blank=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	USERNAME_FIELD = "email_id"
	EMAIL_FIELD = "email_id"
	REQUIRED_FIELDS = ["phone_no", "first_name", "last_name"]

	objects = TheUserManager()

	def __str__(self) -> str:
		return self.first_name + ' ' + self.last_name
