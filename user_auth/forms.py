from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext as _

from .models import User

import re

MODE_CHOICES = (
    ('activation', _('activation link')),
    ('recovery', _('password recovery')),
)

class ForgotActivationForm(forms.Form):
    email = forms.CharField(label=_('email'), max_length=200)
    mode = forms.ChoiceField(choices=MODE_CHOICES, widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder' : _('email'),})
        self.fields['mode'].widget.attrs.update({'checked' : 'checked',})

        for field in self.fields:
            if field != "mode":
                self.fields[field].widget.attrs.update({'class': 'form-control rounded'})
                self.fields[field].requierd = True

    def clean_email(self):
        super().clean()
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email):
            raise forms.ValidationError(_("this email is not registered on the site"))
        return email


class RegisterForm(forms.ModelForm):
    password = forms.CharField(required=True, max_length=32, widget=forms.PasswordInput, label=_("password"))
    password_confirmation = forms.CharField( required=True, max_length=32, widget=forms.PasswordInput, label=_("password_confirmation"))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'placeholder': _(field)})
            self.fields[field].requierd = True

    def clean_email(self):
        cleaned_data = super().clean()
        email = self.cleaned_data['email']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(email) :
            raise forms.ValidationError(_("invalid email-type"))
        if User.objects.filter(email=email) :
            raise forms.ValidationError(_("email is already exist"))
        return email

    def clean_password_confirmation(self) :
        cleaned_data = super().clean()
        password_confirmation = self.cleaned_data['password_confirmation']
        password = self.cleaned_data['password']
        list_ok = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.@#$%*&^%"
        for i in password :
            if i not in list_ok :
                raise ValidationError(_("invalid password type"))
        if len(password_confirmation) < 8 :
            raise forms.ValidationError(_("minimum length of password must be 8 characters"))
        elif password != password_confirmation :
            raise forms.ValidationError(_("password and confirm password does not match"))
        elif password.isnumeric() :
            raise forms.ValidationError(_("password must contain at least one character"))
        return password_confirmation


class LoginForm(forms.Form):
    email = forms.CharField(label=_('email'), max_length=200, required=True)
    password = forms.CharField(label=_("password"), max_length=50, required=True, widget=forms.PasswordInput())
    remember_me = forms.BooleanField(label=_("remember me"), required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder' : _('email'),})
        self.fields['password'].widget.attrs.update({'placeholder' : _('password'),})
        self.fields['remember_me'].widget.attrs.update({'checked' : 'checked',})

        for field in self.fields:
            if field != "remember_me":
                self.fields[field].widget.attrs.update({'class': 'form-control rounded'})
                self.fields[field].requierd = True

    def clean_email(self):
        super().clean()
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email):
            raise forms.ValidationError(_("this email is not registered on the site"))
        return email


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'bio', 'image', 'whatsapp', 'instagram', 'github', 'gitlab']
        widgets = {
            'bio' : forms.Textarea(attrs={'rows': 4,}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        no_req = ['whatsapp', 'instagram', 'github', 'gitlab']
        for field in self.fields:
            self.fields[field].requierd = False
            if field in no_req:
                self.fields[field].widget.attrs.update({'class' : 'form-control p-4 text-left', 'placeholder': _(field)})
            else:
                self.fields[field].widget.attrs.update({'class' : 'form-control p-4', 'placeholder': _(field)})

        self.fields['image'].widget.attrs.update({'class' : 'form-control-file',})
        self.fields['bio'].widget.attrs.update({'placeholder': _("write something about yourself")})


class ChangePasswordForm(forms.Form):
    password = forms.CharField(label=_("Password"), max_length=50, required=True, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label=_("Repeat Password"), max_length=50, required=True, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control p-4', 'placeholder': _("password")})
        self.fields['password_confirmation'].widget.attrs.update({'class': 'form-control p-4', 'placeholder': _("repeat password")})


    def clean_password(self) :
        super().clean()
        password = self.cleaned_data['password']
        if len(password) < 8 :
            raise forms.ValidationError(_("Minimum Length Of Password Must Be 8 Characters"))
        elif password.isnumeric() :
            raise forms.ValidationError(_("Password Must Contain At Least One Character"))
        return password

    def clean_password_confirmation(self):
        super().clean()
        password= self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError(_("Repeat password is not the same as the password "))
        return password_confirmation