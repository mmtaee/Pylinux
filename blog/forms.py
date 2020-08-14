from django import forms
from django.utils.translation import ugettext as _

from base.models import *


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

