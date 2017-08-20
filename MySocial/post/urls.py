from django.conf.urls import url

from . import views

app_name = 'post'

urlpatterns = [
    url(r'^by/(?P<username>[-\w]+)/$', views.UserPost.as_view(), name='post_user'),
    url(r'^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='single'),
    url(r'^by/(?P<username>[-\w]+)/new-post/$', views.CreatePost.as_view(), name='create_post'),
    url(r'^by/(?P<pk>[-\w]+)/delete/$', views.DeletePostView.as_view(), name='delete'),

]