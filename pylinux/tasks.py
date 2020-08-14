from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext as _

from celery import shared_task
import string
import random

from pylinux.methods import account_activation_token
from pylinux.methods import check_profanity
from user_auth.models import User


@shared_task
def send_email_activation(user_pk, domain):
    user = User.objects.get(pk=user_pk)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    template = 'active_link_creator.html'
    subject = 'pylinux activation link'
    message = render_to_string(template, {
        'user': user,
        'domain': domain,
        'uid': uid,
        'token': token,
    })
    try:
        email = EmailMessage(subject, message, to=[user.email])
        email.send()
    except:
        return False

    return True


@shared_task
def send_email_password(user_pk):
    user = User.objects.get(pk=user_pk)
    subject = 'pylinux new password'
    base_password = string.ascii_letters + string.digits
    password = "".join(random.choice(base_password) for x in range(8))
    user.password = make_password(password)
    user.save()
    message = _('your new password is') + f" :  {password}"
    try:
        email = EmailMessage(subject, message, to=[user.email])
        email.send()
    except:
        return False

    return True


@shared_task
def check_profanity_text(text):
    result = check_profanity(text)
    if not result:
        return False
    return True