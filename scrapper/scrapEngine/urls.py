from django.urls import path
from . import views

recent_search = list()

urlpatterns = [
    path('', views.index,name='index'),
    path('jobs/',views.jobs,name='jobs'),
]