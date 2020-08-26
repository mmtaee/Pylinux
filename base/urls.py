from django.urls import path

from .views import *

app_name = 'base'

urlpatterns = [
    path('create/', CreatePostView.as_view(), name='create'),
    path('update/<int:id>/', UpdatePostView.as_view(), name='update'),
    path('user_post/', ListUserPostView.as_view(), name='user_post'),
    path('post_request/<str:action>/<int:id>/', PostRequestManager.as_view(), name='post_request'),
    path('post/<int:id>/', PostDetailView.as_view(), name='post_detail'),

    path('comment/', ListUserCommentView.as_view(), name='user_comment'),
    path('comment_request/<str:action>/<int:id>/', CommentRequestManager.as_view(), name='comment_request'),
    
    path('write/', WriteMessageView.as_view(), name='write_message'),
    path('inbox/', InboxMessageView.as_view(), name='inbox_message'),
    path('message_recive/<int:id>/', DetailReciveMessageView.as_view(), name='detail_recive_message'),
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('contact_us_messages/', ContactUsMessageView.as_view(), name='contact_us_message'),
    path('contact_us_messages_delete/<int:id>/', ContactUsMessageDeleteView.as_view(), name='delete_contact_us_message'),

    path('message_send/<int:id>/', DetailsendMessageView.as_view(), name='detail_send_message'),
    path('message_delete/<int:id>/', InboxDeleteMessage.as_view(), name='delete_message'),
    path('message_reply/<int:id>/', MessageReplyView.as_view(), name='reply_message'),
    path('message_reply_delete/<int:id>/', MessageReplyDeleteView.as_view(), name='delete_reply_message'),
]