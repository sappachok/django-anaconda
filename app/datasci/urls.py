from django.urls import path
from datasci.views import SampleView
from datasci import views

from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('/', views.datasci, name='datasci'),
    path('/project/<str:pid>/', views.project, name='project'),
    path('/editor/<str:pid>/', views.editor, name='editor'),
    path('/editor_process/', views.editor_process, name='editor-process'),
    path('/chartjs/', views.chartjs, name='chartjs'),
    path('/chartjs/api/', views.chart_data, name='chartjs-chart_data'),
    path('/about/', SampleView.as_view(), name='about'),
    path('/client/', views.client_socket, name='client'),
    
]