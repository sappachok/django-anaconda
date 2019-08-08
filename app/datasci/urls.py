from django.urls import path
from datasci.views import SampleView
from datasci import views

from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('/', views.datasci, name='datasci'),
    path('/show/', views.datasci, name='mathpot'),
    path('/about/', SampleView.as_view(), name='about'),
    path('/test/', views.test, name='test'),
]