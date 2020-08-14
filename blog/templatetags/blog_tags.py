from django import template

from base.models import *

register = template.Library()

queryset = Post.objects.filter(publish=True)

@register.simple_tag
def get_category_data():
    datas = {}
    categories = Category.objects.all()
    for category in categories:
        datas[category] = queryset.filter(category_id=category.id).count()
    return datas, queryset.count()

@register.simple_tag
def get_recent_post():
    return queryset.order_by('-create')[:4]

@register.simple_tag
def get_common_tag():
    return Post.tags.most_common()[:10]
