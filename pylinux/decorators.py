from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied
# from functools import wraps

import requests
import redis

from .methods import *


from .methods import *


def check_recaptcha_v3(view_func):

    def wrap(request, *args, **kwargs):
        request.recaptcha_v3_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response_v3')
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success'] and result['score'] >= 0.5:
                request.recaptcha_v3_is_valid = True
            else:
                request.recaptcha_v3_is_valid = False
                messages.error(request, _('invalid') + ' reCAPTCHA')
        return view_func(request, *args, **kwargs)

    return wrap


def check_recaptcha_v2(view_func):

    def wrap(request, *args, **kwargs):
        if request.method == 'POST':
            if 'g-recaptcha-response' in request.POST:
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data = {
                    'secret': settings.RECAPTCHA_SECRET_KEY_V2,
                    'response': recaptcha_response
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()
                if result['success']:
                    request.recaptcha_v2_is_valid = True
                else:
                    request.recaptcha_v2_is_valid = False
                    messages.error(request, _('invalid') + ' reCAPTCHA')
            else:
                request.recaptcha_v2_is_valid = None
        return view_func(request, *args, **kwargs)

    return wrap


def anonymous_required(view_func, redirect_to=None):
    def wrap(request, *args, **kwargs):

        if request.user is not None and request.user.is_authenticated:
            return redirect("/")

        return view_func(request, *args, **kwargs)

    return wrap


def writeruser_required(view_func):
    def wrap(request, *args, **kwargs):

        if request.user.is_anonymous or not request.user.is_writer:
            raise PermissionDenied


        return view_func(request, *args, **kwargs)

    return wrap


def one_time_register(view_func):

    def wrap(request, *args, **kwargs):

        session = request.session
        if session and 'register' in session:
            msg = _("you are already registered on our website") + ". " +\
                  _('if you have forgotten your password, try requesting a new password')
            messages.warning(request, msg)
            return redirect('auth:forgot_activation')

        return view_func(request, *args, **kwargs)

    return wrap


def max_request_user(view_func):

    def wrap(request, *args, **kwargs):
        maxrequestuser = MaxRequestUser(request)
        count = maxrequestuser.get_request_count()
        if count >= 8 :
            msg = _('maximum attempt to request a password or activation link in one day')
            messages.warning(request, msg)
            return redirect("/")
        return view_func(request, *args, **kwargs)

    return wrap


def complete_bio(view_func):

    def wrap(request, *args, **kwargs):
        image_profile = request.user.image.url
        bio = request.user.bio

        if not request.user.username:
            msg = _("choose a username, complete your bio and choose a image for your profile")
            messages.warning(request, msg)

        elif bio is None or bio == "" :
            msg = _("write your bio")
            messages.warning(request, msg)

        elif len(bio) < 10:
            msg = _("complete your bio")
            messages.warning(request, msg)

        elif image_profile == '/media/static/user.jpg':
            msg = _("choose a image for your profile")
            messages.warning(request, msg)

        else:
            return view_func(request, *args, **kwargs)

        return redirect("auth:profile")

    return wrap


def complete_oauth_profile(view_func):

    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.password :
                msg = _("You must first have password")
                messages.warning(request, msg)
                return redirect("auth:change_password")
        return view_func(request, *args, **kwargs)

    return wrap