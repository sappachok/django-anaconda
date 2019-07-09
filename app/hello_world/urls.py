from django.urls import path
from hello_world.views import AboutView
from hello_world import views

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('/about/', AboutView.as_view(), name="about"),
]