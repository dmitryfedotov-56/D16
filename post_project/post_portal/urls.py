from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls import static

urlpatterns = [
    path('', index, name='main_page'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('post_list', PostList.as_view(), name = 'post_list'),
    path('new_post/', PostCreate.as_view(), name='new_post'),
    path('post/<int:pk>', PostDetail.as_view(), name='post'),
    path('post_update/<int:pk>', PostUpdate.as_view(), name='post_update'),
    path('new_comment/<int:pk>', CommentCreate.as_view(), name='new_comment'),
    path('comment_list/', CommentList.as_view(), name='comment_list'),
    path('comment/<int:pk>', CommentDetail.as_view(), name='comment'),
    path('comment_delete/<int:pk>', CommentDelete.as_view(), name='comment_delete'),
    path('accept/<int:pk>', accept, name = 'accept'),
    # path('test/',send_mails, name='test'),
]

