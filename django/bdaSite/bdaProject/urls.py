from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('org/<str:org>/', views.org, name='organization'),
    path('user/<str:userId>/', views.user, name='user'),
    path('org/<str:org>/repo/<str:repo>', views.repo, name='repository'),
]