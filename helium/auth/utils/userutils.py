"""
Utility function for user data.
"""

from random import randint

from django.contrib.auth import get_user_model

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2017, Helium Edu'
__version__ = '1.0.0'


def generate_phone_verification_code():
    code = None
    while not code:
        code = randint(100000, 999999)

        # Ensure the slug does not already exist in the database
        if get_user_model().objects.filter(profile__phone_verification_code=code).exists():
            code = None

    return code


def validate_password(password1, password2):
    if password1 != password2:
        return "You must enter matching passwords."
    else:
        if not password1 or not password2 or len(password2) < 8:
            return "Your password must be at least 8 characters long and contain one letter and one number."

        first_isalpha = password2[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password2):
            return "Your password must be at least 8 characters long and contain one letter and one number."