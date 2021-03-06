from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from datetime import datetime, timedelta
import jdatetime
import matplotlib.pyplot as plt
import io
import urllib, base64
import numpy as np
from dateutil.relativedelta import relativedelta

from base.models import *
from .models import *
from taggit.models import Tag
from .forms import *
from base.forms import *
from pylinux.methods import *
from pylinux.decorators import *
from pylinux.tasks import check_profanity_text
from user_auth.models import User


class HomePageView(View):
    template_name = 'home.html'
    form_class = ContactUsMessageForm

    def get(self, request, *args, **kwargs):
        context = {
            'form' : self.form_class(),
            'staffusers' : User.objects.filter(is_staff=True).order_by("-is_superuser"),
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'site_key_v2': settings.RECAPTCHA_SITE_KEY_V2,
            'recent_blog' : Post.objects.filter(publish=True).order_by('-create')[:4],
            'categories' : Category.objects.all(),

        }
        return render(request, self.template_name, context)


    @method_decorator(check_recaptcha_v3)
    @method_decorator(check_recaptcha_v2)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            message = form.cleaned_data.get('message')
            subject = form.cleaned_data.get('subject')
            result_subject = check_profanity_text.delay(subject).get()
            result = check_profanity_text.delay(message).get()
            if result and result_subject:
                new.save()
            msg = _("your message has been successfully sent")
            messages.success(request, msg)
            return redirect("/")

        context = {
            'form' : form,
            'staffusers' : User.objects.filter(is_staff=True).order_by("-is_superuser"),
            'site_key': settings.RECAPTCHA_SITE_KEY,
            'site_key_v2': settings.RECAPTCHA_SITE_KEY_V2,
            'recent_blog' : Post.objects.filter(publish=True).order_by('-create')[:4],
            'categories' : Category.objects.all(),
        }
        return render(request, self.template_name, context)


class BlogView(ListView):
    template_name = 'blog.html'
    queryset = Post.objects.filter(publish=True).order_by('-title')
    paginate_by = 6


class BlogCategoryView(ListView):
    template_name = 'blog_category.html'
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs.get('id')
        queryset = Post.objects.filter(category_id=id, publish=True).order_by('-title')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category = self.kwargs.get('category')
        context['category_type'] = category
        return context


class TagsView(ListView):
    template_name = 'tags.html'

    def get_queryset(self, *args, **kwargs):
        id = self.kwargs.get('id')
        tags = get_object_or_404(Tag, id=id)
        queryset = Post.objects.filter(tags=tags).order_by('-title')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().order_by('-name')
        context['recent'] = Post.objects.filter(publish=True).order_by('-create')[:4]
        context['tags'] = common_tags = Post.tags.most_common()[:10]
        context['all_tags'] = Tag.objects.all().order_by('-name')
        return context


class PostDetailView(View):
    template_name = 'detail.html'
    form_class = CommentForm


    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        post = get_object_or_404(Post, id=id)
        post.view += 1
        post.save()
        comment = Comment.objects.filter(post=post)
        context = {
            'form' : self.form_class,
            'post' : post,
            'categories' : Category.objects.all().order_by('-name'),
            'recent' : Post.objects.filter(publish=True).order_by('-create')[:4],
            'tags' : Post.tags.most_common()[:10],
            'comments' : comment.order_by('create'),
            'comment_count' : comment.count(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        post = get_object_or_404(Post, id=id)
        form = self.form_class(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            text = form.cleaned_data.get('text')
            result = check_profanity_text(text)
            if result:
                new.user = request.user
                new.post = post
                new.save()
                msg = _('Your comment was sent successfully')
                messages.success(request, msg)
                return redirect('blog:detail', id=id)
            else:
                msg = _("There are insulting words in your comment")
                messages.warning(request, msg)

        comment = Comment.objects.filter(post=post)
        context = {
            'form' : form,
            'post' : post,
            'categories' : Category.objects.all().order_by('-name'),
            'recent' : Post.objects.filter(publish=True).order_by('-create')[:4],
            'tags' : Post.tags.most_common()[:10],
            'comments' : comment.order_by('create'),
            'comment_count' : comment.count(),
        }
        return render(request, self.template_name, context)


class SearchView(TemplateView):
    template_name = 'search.html'


class SitePlotsView(TemplateView):
    template_name = 'site_plots.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        def autolabel(rects, ax):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2.0, 1.0 * height, '%d' % int(height), ha='center', va='bottom')

        def plot_creator(queryset, header):
            day_list = []
            num_list = []
            for query in queryset:
                day = jdatetime.datetime.fromgregorian(datetime=query.date)
                day_list.append(str(day.day) + "/" + day.strftime("%B"))
                num_list.append(query.num)
            ind = np.arange(len(day_list))
            width = 0.2
            fig, ax = plt.subplots()
            plt.suptitle(header)
            plot = ax.bar(ind, num_list, width, color='g', align='center')
            plt.xticks(ind, day_list)
            plt.ylabel('person')
            plt.xlabel('day')
            autolabel(plot, ax)
            fig = plt.gcf()
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            return urllib.parse.quote(string)

        date = datetime.today() + relativedelta(months=-2)
        home = HomeRequest.objects.filter(date__month__gte=date.month).order_by("date")
        blog = BlogRequest.objects.filter(date__month__gte=date.month).order_by("date")

        context['home_plot'] = plot_creator(home, _('Homepage Visitors Plot'))
        context['blog_plot'] = plot_creator(blog, _('Blogpage Visitors Plot'))
        return context


# Ajax
class CommentReportAjax(View):

    def get(self, request, *args, **kwargs):
        if request.is_ajax() and request.user.is_authenticated:
            reason = (request.GET.get("reason", None)).strip()
            comment_id = (request.GET.get("comment_id", None)).strip()
            reporter_id = (request.GET.get("reporter_id", None)).strip()
            if Report.objects.filter(comment_id=comment_id, reporter_id=reporter_id):
                return JsonResponse({'repetitious':True}, status=200)

            report = Report.objects.create(
                comment_id=comment_id,
                reporter_id=reporter_id,
                reason=reason,
            )
            return JsonResponse({'repetitious': False}, status=200)
        return JsonResponse({}, status=400)


class BlogSortAjax(ListView):
    template_name = 'ajax_blog.html'
    paginate_by = 6
    query = None

    def dispatch(self, request, *args, **kwargs):
        if self.request.is_ajax():
            return super().dispatch(request, *args, **kwargs)
        return JsonResponse({}, status=400)

    def get_queryset(self, *args, **kwargs):
        sort_type = (self.request.GET.get("sortType", None)).strip()
        self.query = queryset = Post.objects.filter(publish=True).order_by(sort_type)
        if self.request.GET.get("pageNumber", None):
            page_number = self.request.GET.get("pageNumber", None)
            paginator = Paginator(queryset, self.paginate_by)
            result = paginator.get_page(page_number)
            return result
        else:
            return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_number = self.request.GET.get("pageNumber", None)
        if page_number:
            context['page_number'] = self.request.GET.get("pageNumber").strip()

        page_range = Paginator(self.query, self.paginate_by).page_range
        if len(page_range) > 1:
            context['page_range'] = page_range
        return context


class BlogCategorySortAjax(ListView):
    template_name = 'ajax_blog_category.html'
    paginate_by = 6
    query = None

    def dispatch(self, request, *args, **kwargs):
        if self.request.is_ajax():
            return super().dispatch(request, *args, **kwargs)
        return JsonResponse({}, status=400)

    def get_queryset(self, *args, **kwargs):
        sort_type = (self.request.GET.get("sortType", None)).strip()
        category_type = (self.request.GET.get("category_type", None)).strip()

        self.query = queryset = Post.objects.filter(category__name=category_type,publish=True).order_by(sort_type)
        if self.request.GET.get("pageNumber", None):
            page_number = self.request.GET.get("pageNumber", None)
            paginator = Paginator(queryset, self.paginate_by)
            result = paginator.get_page(page_number)
            return result
        else:
            return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_number = self.request.GET.get("pageNumber", None)
        if page_number:
            context['page_number'] = self.request.GET.get("pageNumber").strip()

        page_range = Paginator(self.query, self.paginate_by).page_range
        if len(page_range) > 1:
            context['page_range'] = page_range
        context['category_type'] = (self.request.GET.get("category_type", None)).strip()
        return context


class SearchAjax(View):
    template_name = 'search_result.html'

    def get(self, request, *args, **kwargs):
        if self.request.is_ajax():
            search = (self.request.GET.get("search", None)).strip()
            posts = Post.objects.filter(
                Q(title__contains=search) |
                Q(category__name__contains=search) |
                Q(user__username__contains=search) |
                Q(summary__contains=search) |
                Q(text__contains=search)
            ).order_by('title')
            context = {
                'posts' : posts,
            }
            return render(request, self.template_name, context)
        return JsonResponse({}, status=400)
