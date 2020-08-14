from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse

from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(_("name"), max_length=200)
    image = models.ImageField(upload_to='category/')

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(_("title"), max_length=300)
    summary = models.TextField()
    text = RichTextUploadingField()
    image = models.ImageField(upload_to='post/')
    image_source = models.URLField(null=True, blank=True)
    study = models.PositiveIntegerField(default=5)
    create = models.DateTimeField(_("create time"), auto_now_add=True)
    last_update = models.DateTimeField(_("last update"), auto_now=True)
    view = models.PositiveIntegerField(null=True, blank=True, default=0)
    slug = models.SlugField(unique=True, max_length=100)
    commenting = models.BooleanField(_("commenting"), default=True, help_text="if checked: post commenting is disabled")
    tags = TaggableManager()
    publish = models.BooleanField(_("publish"), default=False)

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("base:post_detail", kwargs={'id': self.id})

    def get_absolute_url_blog(self):
        return reverse("blog:detail", kwargs={'id': self.id})


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = RichTextField(config_name='comment')
    create = models.DateTimeField(_("create time"), auto_now_add=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return 'comment: ' + self.user.username


class Messaging(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="sender")
    reciver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="reciver")
    create = models.DateTimeField(_("create time"), auto_now_add=True)
    subject = models.CharField(_("subject"), max_length=500)
    message = RichTextField(config_name='message')
    seen = models.BooleanField(_("seen"), default=False)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        return f'sender : {self.sender}, reciver : {self.reciver}'

    def get_absolute_url_reciver(self):
        return reverse('base:detail_recive_message', kwargs={'id' : self.id, })

    def get_absolute_url_sender(self):
        return reverse('base:detail_send_message', kwargs={'id' : self.id, })


class ReplyMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    messaging = models.ForeignKey(Messaging, on_delete=models.CASCADE)
    message = RichTextField(config_name='message')
    create = models.DateTimeField(_("create time"), auto_now_add=True)

    class Meta:
        verbose_name = _("reply")
        verbose_name_plural = _("replies")

    def __str__(self):
        return self.sender.username



REPORT_CHOISES = (
                ('prof', _('profanity')),
                ('adve', _('advertising')),
                ('spam', _('spam')),
                )


class Report(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    create = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=4, choices=REPORT_CHOISES)


    class Meta:
        verbose_name = _("report")
        verbose_name_plural = _("reports")

    def __str__(self):
        return self.reporter.username


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()


    class Meta:
        verbose_name = _("contact us")
        verbose_name_plural = _("contact us")

    def __str__(self):
        return self.name
