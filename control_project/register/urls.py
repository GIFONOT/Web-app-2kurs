from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('info', views.info, name='info'),
    path('contact', views.con, name='con'),

    path('user/<path:id>/', views.user, name='user'),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout')
]
