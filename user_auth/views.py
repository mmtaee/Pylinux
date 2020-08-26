from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.http import Http404
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, update_session_auth_hash

from .forms import *
from pylinux.decorators import *
from pylinux.backends import backend
from pylinux.methods import account_activation_token
from pylinux.tasks import *


class ForgotActivationView(View):
    template_name = 'forgot_activation.html'
    form_class = ForgotActivationForm

    @method_decorator(never_cache)
    @method_decorator(max_request_user)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'site_key_v2': settings.RECAPTCHA_SITE_KEY_V2,
        }
        return render(request, self.template_name, context)

    @method_decorator(check_recaptcha_v3)
    @method_decorator(check_recaptcha_v2)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid() and request.recaptcha_v3_is_valid :
            if request.recaptcha_v2_is_valid or request.recaptcha_v2_is_valid is None:
                email = request.POST.get('email')
                mode = request.POST.get('mode')
                user = get_object_or_404(User, email=email)

                if mode == 'activation' and not user.is_active:
                    domain = get_current_site(request).domain
                    send = send_email_activation.delay(user.pk, domain).get()
                    if send:
                        msg = _('an activation code has been sent to your email')
                        messages.success(request, msg)
                        maxrequestuser = MaxRequestUser(request)
                        maxrequestuser.add_request_count()
                        return redirect('/')
                    else:
                        msg = _('email has not been sent') + " " + _('try again')
                        messages.error(request, msg)

                elif mode == 'activation' and  user.is_active:
                    msg = _('your account is active') + ". " +\
                          _('if you have forgotten your password, try requesting a new password')
                    messages.error(request, msg)
                    maxrequestuser = MaxRequestUser(request)
                    maxrequestuser.add_request_count()

                elif mode == 'recovery':
                    send = send_email_password.delay(user.pk).get()
                    if send:
                        msg = _('new password has been sent to your email')
                        messages.success(request, msg)
                        maxrequestuser = MaxRequestUser(request)
                        maxrequestuser.add_request_count()
                        return redirect('auth:login')
                    else:
                        msg = _('email has not been sent') + ". " + _('try again')
                        messages.error(request, msg)
        context = {
            'form': form,
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'site_key_v2': settings.RECAPTCHA_SITE_KEY_V2,
        }
        return render(request, self.template_name, context)


class Activation(View):

    @method_decorator(anonymous_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        uidb64 = self.kwargs.get('uidb64', None)
        token = self.kwargs.get('token', None)
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='pylinux.backends.EmailBackend')
            msg = _('your registration and login has been completed')
            messages.success(request ,msg)
            return redirect('/')
        else:
            raise Http404("This link has expired")


class RegisterView(View):
    template_name = 'register.html'
    form_class = RegisterForm

    @method_decorator(never_cache)
    @method_decorator(one_time_register)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'site_key_v2': settings.RECAPTCHA_SITE_KEY_V2,
        }
        return render(request, self.template_name, context)

    @method_decorator(check_recaptcha_v3)
    @method_decorator(check_recaptcha_v2)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid() and request.recaptcha_v3_is_valid :
            if request.recaptcha_v2_is_valid or request.recaptcha_v2_is_valid is None:
                ip = request.META.get('REMOTE_ADDR')
                user = form.save(commit=False)
                password = form.cleaned_data.get('password')
                user.password = make_password(password)
                user.is_active = False

                request.session['register'] = 'True'
                request.session.modified = True

                user.save()
                domain = get_current_site(self.request).domain
                send = send_email_activation.delay(user.pk, domain).get()
                if send:
                    msg = _('an activation link has been sent to your email')
                    messages.success(request, msg)
                    return redirect("/")
                else:
                    msg = _('email has not been sent') + " " + _('try again from activation section')
                    messages.error(request, msg)
                    return redirect('auth:forgot_activation')
        context = {
            'form': form,
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'site_key_v2': settings.RECAPTCHA_SITE_KEY_V2,
        }
        return render(request, self.template_name, context)


class LoginView(View):
    template_name = 'login.html'
    form_class = LoginForm

    @method_decorator(never_cache)
    # TODO : active in deployment
    # @method_decorator(one_time_register)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(anonymous_required)
    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class,
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'site_key_v2': settings.RECAPTCHA_SITE_KEY_V2,
        }
        return render(request, self.template_name, context)


    @method_decorator(check_recaptcha_v3)
    @method_decorator(check_recaptcha_v2)
    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid() and request.recaptcha_v3_is_valid :
            if request.recaptcha_v2_is_valid or request.recaptcha_v2_is_valid is None:
                next_to = request.GET.get('next', None)
                email = request.POST.get('email')
                password = request.POST.get('password')
                remember_me = request.POST.get('remember_me')
                if remember_me:
                    request.session.set_expiry(2592000)
                user = backend.authenticate(email=email, password=password)
                if user and user.is_active:
                    login(request, user, backend='pylinux.backends.EmailBackend')
                    msg = _('you have successfully logged in')
                    messages.success(request, msg)
                    if next_to:
                        return redirect(next_to)
                    return redirect('/')
                elif user and not user.is_active:
                    msg = _('your account has not been activated') + ". " +\
                          _("If you did not receive the activation email, try again with this link below")
                    messages.error(request, msg)
                    return redirect('auth:forgot_activation')

            msg = _('invalid email or password')
            messages.error(request, msg)

        context = {
            'form': form,
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'site_key_v2': settings.RECAPTCHA_SITE_KEY_V2,
        }
        return render(request, self.template_name, context)


class LogoutView(RedirectView):
    url = "/"

    @method_decorator(complete_oauth_profile)
    def get(self, request, *args, **kwargs):
        # conflict with  user.is_online in signals.py
        if request.user.is_anonymous:
            return redirect("/")

        logout(request)
        return super().get(request, *args, **kwargs)


class ProfileView(View):
    template_name = 'profile.html'
    form_class = ProfileForm

    @method_decorator(login_required(login_url=reverse_lazy('auth:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'form' : self.form_class(instance=request.user)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            update_session_auth_hash(request, user)
            msg = _('your profile changed successfully')
            messages.success(request, msg)
            return redirect("/")
        context = {
            'form' : form,
        }
        return render(request, self.template_name, context)


class ChangePasswordView(FormView):
    template_name = 'change_password.html'
    form_class = ChangePasswordForm
    success_url = "/"

    @method_decorator(login_required(login_url=reverse_lazy('auth:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = get_object_or_404(User, id=self.request.user.id)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        update_session_auth_hash(self.request, user)
        msg = _('password changed successfully')
        messages.success(self.request, msg)
        return super().form_valid(form)



# handlers

handler_templates = {
    400 : 'handler/400.html',
    403 : 'handler/403.html',
    404 : 'handler/404.html',
    500 : 'handler/500.html',
}

class ErrorHandler(TemplateView):
    template_name = ''
    status_code = None

    def dispatch(self, request, *args, **kwargs):
        self.template_name = handler_templates[self.status_code]
        return super().dispatch(request, *args, **kwargs)


def handler500(request):
    view = ErrorHandler.as_view(status_code=500)
    return view(request)


class HandlerTest(TemplateView):
    template_name = ''

    def dispatch(self, request, *args, **kwargs):
        status_code = kwargs.get('status_code')
        self.template_name = handler_templates[status_code]
        return super().dispatch(request, *args, **kwargs)
