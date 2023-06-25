from django.urls import path, re_path
from . import views

urlpatterns = [
    path('adduser/', views.add_user, name='add_user'),
    path('addproject/', views.add_project, name='add_project'),
    path('addprojperson/', views.add_project_person, name='add_project_person'),
    path('addmainuser/', views.add_main_user, name='add_main_user'),

    path('usercheck/', views.user_check, name='user_check'),
    path('savestatus/', views.save_status, name='save_status'),

    path('download-report/', views.generate_report, name='download_report'),

]