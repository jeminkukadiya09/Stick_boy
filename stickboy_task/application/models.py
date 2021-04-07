from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):

	def create_user(self,email,password,**extra_fields):
		if not email:
			raise ValueError('Users must have an email address')


		user = self.model(email = self.normalize_email(email))
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using = self._db)
		return user


	def create_superuser(self,email,password):

		if password is None:
			raise TypeError('superuser must have a password')

		user = self.create_user(email,password)
		user.is_superuser = True
		user.is_staff = True
		user.save()

		return user


class User(AbstractBaseUser, PermissionsMixin):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
	last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)	
	email = models.CharField(unique=True,max_length=50)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects =UserManager()

	def __str__(self):
		return self.email

	class Meta:
		db_table = "login"


	