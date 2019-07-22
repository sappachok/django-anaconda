from django.urls import path
from hello_world.views import AboutView
from hello_world import views

from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('/getimage/', views.setPlt, name='setPlt'),
    path('/about/', AboutView.as_view(), name="about"),
    path('/call_func/', views.call_func, name='call_func'),
    path('/call_pot/', views.call_pot, name='call_pot'),
]