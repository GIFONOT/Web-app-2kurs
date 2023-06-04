from django.urls import path, re_path
from . import views

urlpatterns = [
    #re_path(r'^user/(?P<id>.+)/adduser/$', views.add_user, name='add_user'),
    path('adduser/', views.add_user, name='add_user'),
    path('addproject/', views.add_project, name='add_project')

]