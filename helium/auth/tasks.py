import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

from conf.celery import app
from helium.common.utils import commonutils, metricutils

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.3.8'

logger = logging.getLogger(__name__)


@app.task
def send_verification_email(email, username, verification_code):
    if settings.DISABLE_EMAILS:
        logger.warning('Emails disabled. Verification code: {}'.format(verification_code))
        return

    commonutils.send_multipart_email('email/verification',
                                     {
                                         'PROJECT_NAME': settings.PROJECT_NAME,
                                         'username': username,
                                         'verification_code': verification_code,
                                         'site_url': settings.PLATFORM_HOST,
                                         'verify_url': reverse('verify'),
                                     },
                                     'Verify Your Email Address with Helium', [email])


@app.task
def send_registration_email(email):
    if settings.DISABLE_EMAILS:
        logger.warning('Emails disabled. Welcome email not sent.')
        return

    commonutils.send_multipart_email('email/register',
                                     {
                                         'PROJECT_NAME': settings.PROJECT_NAME,
                                         'site_url': settings.PLATFORM_HOST,
                                         'login_url': reverse('login'),
                                     },
                                     'Welcome to Helium', [email], [settings.DEFAULT_FROM_EMAIL])


@app.task
def send_password_reset_email(email, temp_password):
    if settings.DISABLE_EMAILS:
        logger.warning('Emails disabled. Reset password: {}'.format(temp_password))
        return

    metricutils.increment('task.user.password-reset')

    commonutils.send_multipart_email('email/forgot',
                                     {
                                         'password': temp_password,
                                         'site_url': settings.PLATFORM_HOST,
                                         'settings_url': reverse('settings'),
                                         'support_url': reverse('support'),
                                     },
                                     'Your Helium Password Has Been Reset', [email])


@app.task
def delete_user(user_id):
    # The instance may no longer exist by the time this request is processed, in which case we can simply and safely
    # skip it
    try:
        user = get_user_model().objects.get(pk=user_id)

        user.delete()
    except get_user_model().DoesNotExist:
        logger.info('User {} does not exist. Nothing to do.'.format(user_id))

        return
