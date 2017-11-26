"""
Manager for the User model.
"""

import logging

from django.contrib.auth.models import BaseUserManager

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '0.5.0'

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Create a new user with the given username, password, and email.

        :param username: the username for the user
        :param email: the email for the new user
        :param password: the password for the new user
        :return: the created object
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
                email=self.normalize_email(email),
                username=username
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """
        Create a new super user with admin privileges.

        :param username: the username for the user
        :param email: the email for the new user
        :param password: the password for the new user
        :return: the created object
        """
        user = self.create_user(username=username,
                                email=email,
                                password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user
