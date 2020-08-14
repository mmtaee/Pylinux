from django import template

from base.models import *
from user_auth.models import *

register = template.Library()


@register.simple_tag
def get_sidebar_badge(user):
    context = {
        'post' : Post.objects.filter(user=user,publish=False).count(),
        'reported_comment' : Report.objects.filter(comment__post__user=user).count(),
        'recive' :Messaging.objects.filter(reciver=user, seen=False).count(),
        'send' :Messaging.objects.filter(sender=user, seen=False).count(),
        'contact_message' : ContactUs.objects.all().count(),
    }
    return context
