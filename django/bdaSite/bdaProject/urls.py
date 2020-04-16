from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('org/<str:org>/', views.org, name='organization'),
]