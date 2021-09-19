from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager
from django.db import models


# class UserManager(BaseUserManager):
#     use_in_migrations = True

#     def create_user(self, username, email, password, first_name, last_name, **extra_fields):
#         """
#         Create and save a user with the given username, email, and password.
#         """
#         if not username:
#             raise ValueError('У пользователя должен быть username')
#         if not email:
#             raise ValueError('У пользователя должен быть email')
#         if not first_name:
#             raise ValueError('У пользователя должно быть имя')
#         if not last_name:
#             raise ValueError('У пользователя должна быть фамилия')
#         email = self.normalize_email(email)
#         username = self.model.normalize_username(username)
#         last_name = self.last_name
#         user = self.model(
#             username=username, 
#             email=email, 
#             last_name=last_name,
#             fist_name=first_name,
#             **extra_fields
#             )
#         # user.last_name = last_name
#         # user.first_name = first_name
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, first_name=None, last_name=None, email=None, password=None):
#         user = self.create_user(
#             username, 
#             password, 
#             first_name, 
#             last_name,
#             is_staff=True,
#             is_admin=True
#         )
#         return user
    
#     def create_staffuser(self, username, first_name=None, last_name=None, email=None, password=None):
#         user = self.create_user(
#             username,
#             password,
#             first_name,
#             last_name,
#             is_staff=True,
#             is_admin=False
#         )
#         return user


# class User(AbstractBaseUser):
#     email = models.EmailField(unique=True, max_length=255)
#     username = models.CharField(unique=True, max_length=50)
#     first_name = models.CharField(max_length=255, null=True)
#     last_name = models.CharField(max_length=255, null=True)
    
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['username']
    
#     objects = UserManager()
    
    
