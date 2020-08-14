from django.contrib import admin

from .models import *


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Messaging)
admin.site.register(ReplyMessage)
admin.site.register(Report)
admin.site.register(ContactUs)
