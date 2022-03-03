from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Comment
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, PostUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from .filters import CommentFilter
from django.shortcuts import redirect
from django.conf import settings


# this import is necessary for e-mail sending
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

SOURCE_EMAIL = 'dfedotov-skillfactory@yandex.ru'

# date and time
import datetime
from datetime import datetime
from datetime import timedelta


# for tests only
def stub(request):
    return HttpResponseNotFound('<h1>Page not found</h1>')


@login_required
def index(request):
    return render(request, 'index.html')


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-id']


class PostCreate(LoginRequiredMixin, CreateView):
    template_name = 'new_post.html'
    form_class = PostForm
    success_url = '/post_list'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('pk')
        context['post_id'] = post_id
        post = Post.objects.get(id = post_id)
        context['is_author'] = post.user == self.request.user
        context['link'] = None
        if post.content:
            base_dir = str(settings.BASE_DIR)
            content = str(post.content)
            slash = '\\'
            link = base_dir + slash + content
            print(link)
            context['link'] = link
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'post_update.html'
    form_class = PostUpdateForm
    queryset = Post.objects.all()
    success_url = '/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk = id)


# new comment created, send email to the post author
def comment_created(instance):

    html_content = render_to_string(  # html to send    # html to send
        'comment_created.html',
        {
            'post_title': instance.post.title,
            'comment_author': instance.user.username,
            'comment_text': instance.text,
            'comment_id': instance.id
        }
    )

    msg = EmailMultiAlternatives(                       # the message itself
        subject='news_portal',
        body='test',
        from_email=SOURCE_EMAIL,
        to=[instance.post.user.email]
    )
    
    msg.attach_alternative(html_content, "text/html")   # html content
    msg.send()                                          # send message
        

class CommentCreate(LoginRequiredMixin, CreateView):
    template_name = 'new_comment.html'
    form_class = CommentForm
    context_object_name = 'comment'
    success_url = '/post_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('pk')
        post = Post.objects.get(id=post_id)
        post_title = post.title
        context['post_title'] = post_title
        return context

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        self.post_id = id
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        post = Post.objects.get(id=self.post_id)
        self.object.post = post
        self.post_title = post.title
        self.object.user = self.request.user
        self.object.save()
        comment_created(self.object)
        return HttpResponseRedirect(self.get_success_url())


class CommentList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comment_list.html'
    context_object_name = 'comments'
    ordering = ['-id']

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(post__user = user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CommentDetail(LoginRequiredMixin, DetailView):
    template_name = 'comment.html'
    context_object_name = 'comment'
    queryset = Comment.objects.all()


class CommentDelete(LoginRequiredMixin, DeleteView):
    template_name = 'comment_delete.html'
    context_object_name = 'comment'
    queryset = Comment.objects.all()
    success_url = '/comment_list/'


# comment accepted, send email to the comment author
def comment_accepted(instance):
    html_content = render_to_string(  # html to send    # html to send
        'comment_accepted.html',
        {
            'post_title': instance.post.title,
        }
    )

    msg = EmailMultiAlternatives(                       # the message itself
        subject='news_portal',
        body='test',
        from_email=SOURCE_EMAIL,
        to=[instance.user.email]
    )

    msg.attach_alternative(html_content, "text/html")   # html content
    msg.send()                                          # send message


@login_required                                         # accept comment
def accept(request, pk):
    print(pk)
    comment = Comment.objects.get(id = pk)
    comment.status = True
    comment.save()
    comment_accepted(comment)
    return redirect('/comment_list/')


# send new posts to the users
def send_news():
    old_date = datetime.now() - timedelta(days=1)  # previous date
    new_posts = Post.objects.filter(time_stamp__range=[old_date, datetime.now()])

    if new_posts:
        html_content = render_to_string('new_list.html', {'new_posts': new_posts})

        msg = EmailMultiAlternatives(                       # the message itself
            subject='news_portal',
            body='test',
            from_email=SOURCE_EMAIL,
            to=[]
        )

        users = User.objects.all()                          # mail addresses
        for user in users:
            if user.username != 'admin':
                msg.to.append(user.email)

        print(new_posts)
        print(msg.to)

        msg.attach_alternative(html_content, "text/html")  # html content
        msg.send()                                         # send message


"""
@login_required
def send_mails(request):
    send_news()
    return redirect('/')
"""

"""
class UserInformer():

    def __init__(self):
        old_date = datetime.now() - timedelta(days=1)       # new posts
        self.new_posts = Post.objects.filter(time_stamp__range=[old_date, datetime.now()])

    def send_news(self):
        if self.new_posts:
            html_content = render_to_string('new_list.html', {'new_posts': self.new_posts})

            msg = EmailMultiAlternatives(                       # the message itself
                subject='news_portal',
                body='test',
                from_email=SOURCE_EMAIL,
                to=[]
            )

            users = User.objects.all()
            for user in users:
                msg.to.append(user.username)

            print(self.new_posts)
            print()
 
            msg.attach_alternative(html_content, "text/html")   # html content
            msg.send()                                          # send message
"""

