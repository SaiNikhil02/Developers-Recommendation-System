
from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('create_project/', views.createProject, name='create-project'),
    path('update_project/<str:pk>/', views.updateProject, name='update-project'),
    path('delete_project/<str:pk>/', views.deleteProject, name='delete-project'),
]