from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.http import Http404, JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.conf import settings
from django.utils import translation
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.db.models import Count


from taggit.models import Tag
from datetime import timedelta
from random import randint

from .models import *
from .forms import *
from pylinux.decorators import *


class CreatePostView(FormView):
    template_name = 'create_post.html'
    form_class = CreatePostForm
    success_url = None

    @method_decorator(complete_bio)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        new = form.save(commit=False)
        new.user = self.request.user
        new.slug = slugify(new.title + str(randint(10000, 99999)))
        new.save()
        form.save_m2m()
        # delete unused tag
        Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
        msg = _('post created successfully')
        messages.success(self.request, msg)
        self.success_url = reverse_lazy('base:post_detail', kwargs={'id' : new.id})
        return super().form_valid(form)


class UpdatePostView(UpdateView):
    template_name = 'update.html'
    form_class = CreatePostForm
    success_url = None

    @method_decorator(complete_bio)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        obj = get_object_or_404(Post, id=id)
        return obj

    def form_valid(self, form):
        edit = form.save(commit=False)
        old_tags = Tag.objects.filter(slug=edit.slug)
        old_tags.delete()
        edit.save()
        form.save_m2m()
        # delete unused tag
        Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
        msg = _('post updated successfully')
        messages.success(self.request, msg)
        self.success_url = reverse_lazy('base:post_detail', kwargs={'id' : edit.id})
        return super().form_valid(form)


class ListUserPostView(ListView):
    template_name = 'post.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        if not self.request.user.is_staff:
            posts = Post.objects.filter(user=self.request.user).order_by('-create', '-last_update')
        else:
            posts = Post.objects.all().order_by('-create', '-last_update', '-user')
        return posts


class PostRequestManager(View):

    def get(self, request, *args, **kwargs):
        action = self.kwargs.get('action')
        post_id = self.kwargs.get('id')
        redirect_to = request.GET.get('next', None)
        post = get_object_or_404(Post, id=post_id)

        if action == 'no_pub':
            post.publish = False
            post.save()
            msg = _('post will not be published')
            messages.warning(request, msg)

        elif action == 'pub':
            post.publish = True
            post.save()
            msg = _('post will be published')
            messages.success(request, msg)

        elif action == 'delete':
            post.delete()
            msg = _('post deleted successfully')
            messages.success(request, msg)

        else:
            raise Http404()

        if redirect_to:
            return redirect(redirect_to)
        return redirect('base:user_post')


class ListUserCommentView(ListView):
    template_name = 'comment.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):

        if self.request.user.is_staff:
            queryset = Report.objects.all().order_by('-create')

        else:
            queryset = Report.objects.filter(comment__post__user=self.request.user).order_by('-create')
        return queryset


class CommentRequestManager(View):

    def get(self, request, *args, **kwargs):
        action = self.kwargs.get('action')
        id = self.kwargs.get('id')
        redirect_to = request.GET.get('next', None)

        if action == 'del':
            comment = get_object_or_404(Comment, id=id)
            comment.delete()
            msg = _('the comment has been deleted')


        elif action == 'del_report':
            report = get_object_or_404(Report, id=id)
            report.delete()
            msg = _('the report has been deleted')

        else:
            raise Http404()

        messages.success(request, msg)
        if redirect_to is None:
            redirect_to = reverse('base:user_comment')
        return redirect(redirect_to)


class WriteMessageView(View):
    template_name = 'message/write.html'
    form_class = MessagingForm

    def get(self, request, *args, **kwargs):
        context = {
            'form' : self.form_class(user=request.user),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, user=request.user)
        if form.is_valid():
            new = form.save(commit=False)
            new.sender = self.request.user
            new.save()
            msg = _('the message was successfully sent to') + f" : {new.reciver}"
            messages.success(request, msg)
            return redirect('base:write_message')
        context = {
            'form' : form,
        }
        return render(request, self.template_name, context)


class InboxMessageView(ListView):
    template_name = 'message/inbox.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        query = Messaging.objects.filter(reciver=self.request.user).order_by('seen','-create')
        return query


class SendMessageView(ListView):
    template_name = 'message/send.html'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        query = Messaging.objects.filter(sender=self.request.user).order_by('-create')
        return query


class DetailReciveMessageView(DetailView):
    template_name = 'message/detail_recive.html'

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        message = get_object_or_404(Messaging, id=id)
        message.seen = True
        message.save()
        return message


class DetailsendMessageView(DetailView):
    template_name = 'message/detail_send.html'

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        message = get_object_or_404(Messaging, id=id)
        return message


class InboxDeleteMessage(RedirectView):
    url = reverse_lazy('base:inbox_message')

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        _message = get_object_or_404(Messaging, id=id)
        _message.delete()
        msg = _('message deleted successfully')
        messages.success(request, msg)
        return redirect(self.url)


class PostDetailView(DetailView):
    template_name = 'post_detail.html'

    def get_object(self, *args, **kwargs):
        id = self.kwargs.get('id')
        post = get_object_or_404(Post, id=id)
        return post


class MessageReplyView(FormView):
    template_name = 'message/reply.html'
    form_class = ReplyMessageForm
    success_url = ""

    def get(self, request, *args, **kwargs):
        message_id = self.kwargs.get('id')
        self._message = get_object_or_404(Messaging, id=message_id)
        context = {
            'form': self.form_class(),
            'message': self._message,
        }
        return render(request, self.template_name, context)

    def form_valid(self, form):
        message_id = self.kwargs.get('id')
        self.success_url = self.request.GET.get('next')
        self._message = get_object_or_404(Messaging, id=message_id)
        new = form.save(commit=False)
        new.messaging = self._message
        new.sender = self.request.user
        new.save()
        msg = _('reply has been send to') + new.messaging.sender.username
        messages.success(self.request, msg)
        return super().form_valid(form)


class MessageReplyDeleteView(View):

    def get(self, request, *args, **kwargs):
        reply_id = self.kwargs.get('id')
        redirect_to = request.GET.get('next')
        reply = get_object_or_404(ReplyMessage, id=reply_id)
        if reply.sender == request.user :
            reply.delete()
            msg = _('reply deleted successfully')
            messages.success(request,msg)
        return redirect(redirect_to)


class ContactUsMessageView(ListView):
    template_name = 'message/contact_us_message.html'
    queryset = ContactUs.objects.all()
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        if request.user.username.lower() != 'masoud':
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class ContactUsMessageDeleteView(RedirectView):
    url = reverse_lazy('base:contact_us_message')

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        contact_us = get_object_or_404(ContactUs, id=id)
        contact_us.delete()
        return redirect(self.url)
