from django import forms
from django.utils.translation import ugettext as _

from .models import *
from user_auth.models import *


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', "category", 'summary', 'text', 'image', 'tags', 'study', 'publish', 'commenting', 'image_source']
        widgets = {
            'summary' : forms.Textarea(attrs={'rows': 4,}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            remove = ['image', 'publish', 'study', 'commenting']
            if field not in remove:
                self.fields[field].widget.attrs.update({'class' : 'form-control',})
        self.fields['tags'].widget.attrs.update({'data-role' : "tagsinput",})
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['summary'].widget.attrs.update({'placeholder': _('write a summary of your post in 4 lines').title()})
        self.fields['publish'].requierd = False
        self.fields['commenting'].requierd = False
        self.fields['study'].widget.attrs.update({'class' : 'form-control-lg w-100','min' : 3, 'max':60,})
        self.fields['image_source'].widget.attrs.update({'placeholder': "url".title(),})


class MessagingForm(forms.ModelForm):

    class Meta:
        model = Messaging
        fields = ['reciver', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['reciver'] = forms.ModelChoiceField(
                            queryset=User.objects.exclude(username=user.username),
                            required=True,
                            )
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control',})


class ContactUsMessageForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'message':
                self.fields[field].widget.attrs.update({'class' : 'form-control', 'placeholder': _("message"), 'rows' : 7, 'cols' : 30,})
            else:
                self.fields[field].widget.attrs.update({'class' : 'form-control', 'placeholder': _(field)})
            self.fields[field].requierd = True


class ReplyMessageForm(forms.ModelForm):

    class Meta:
        model = ReplyMessage
        fields = ['message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class' : 'form-control',})