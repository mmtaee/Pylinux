from django.urls import path

from .views import *

app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('home/', HomePageView.as_view()),
    path('blog/', BlogView.as_view(), name='blog'),
    path('search/', SearchView.as_view(), name='search'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),


    path('tags/<str:slug>/', TagsView.as_view(), name='tags'),
    path('detail/<int:id>/', PostDetailView.as_view(), name='detail'),
    path('blog/#<int:id>@<str:category>/', BlogCategoryView.as_view(), name='blog_category'),

    # Ajax
    path("ajax/comment_report/", CommentReportAjax.as_view()),
    path("ajax/blog_sort/", BlogSortAjax.as_view()),
    path("ajax/search/", SearchAjax.as_view()),
    path("ajax/blog_category_sort/", BlogCategorySortAjax.as_view()),


]