from django.urls import path
from smartcv import views

from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('/', views.smartcv, name='smartcv'),
    path('/show/', views.show, name='show'),
]