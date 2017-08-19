from django.conf.urls import url

from . import views

app_name = 'post'

urlpatterns = [
    url(r'^by/(?P<username>[-\w]+)/$', views.UserPost.as_view(), name='user'),
    url(r'^by/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='single'),
    url(r'^by/new-post$', views.CreatePost.as_view(), name='create_post'),
    url(r"delete/(?P<pk>\d+)/$",views.DeletePost.as_view(),name="delete"),

]