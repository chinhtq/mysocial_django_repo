from django.conf.urls import url

from . import views

app_name = 'groups'

urlpatterns = [
    url(r"^$", views.ListGroups.as_view(), name="all"),
    url(r"^post/in/(?P<slug>[-\w]+)/$", views.SingleGroups.as_view(), name="single"),
    url(r"^join/(?P<slug>[-\w]+)/$", views.JoinGroup.as_view(), name="join"),
    url(r"^leave/(?P<slug>[-\w]+)/$", views.LeaveGroup.as_view(), name="leave"),
    url(r"^create/$", views.CreateGroup.as_view(), name="create"),

]