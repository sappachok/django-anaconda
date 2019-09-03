from django.urls import path
from datasci.views import SampleView
from datasci import views

from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('/', views.datasci, name='datasci'),
    path('/project/<str:pid>/', views.project, name='project'),
    path('/chartjs/', views.chartjs, name='chartjs'),
    path('/chartjs/line_chart_json', views.line_chart_json, name='line_chart_json'),
    path('/about/', SampleView.as_view(), name='about'),
]