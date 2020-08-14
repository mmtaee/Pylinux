from django import template

from base.models import *

register = template.Library()


class CommentQuery(object):
    def __init__(self):
        self.queryset = Comment.objects.all()

    def get_queryset(self):
        return self.queryset

comments = CommentQuery()

@register.simple_tag
def get_comment_count(post_id):
    query = comments.get_queryset()
    return query.filter(post_id=post_id).count()


@register.simple_tag
def get_replies(messaging_id):
    replies = ReplyMessage.objects.filter(messaging_id=messaging_id).order_by('create')
    return replies