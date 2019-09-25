from django.urls import path
from datasci.views import SampleView
from datasci import views

from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('/', views.datasci, name='datasci'),
    path('/project/<str:pid>/', views.project_ex, name='project'),
    path('/project_ex/<str:pid>/', views.project_ex2, name='project-ex'),
    path('/project_preview/<str:pid>/', views.project_preview, name='project-preview'),
    path('/editor/<str:pid>/', views.editor, name='editor'),
    path('/editor_process/', views.editor_process, name='editor-process'),
    path('/get-output/', views.get_interactive_output, name='get-output'),
    path('/chartjs/', views.chartjs, name='chartjs'),
    path('/chartjs/api/', views.chart_data, name='chartjs-chart_data'),
    path('/about/', SampleView.as_view(), name='about'),
    path('/kill_process/<int:pid>/', views.kill_process, name='kill-process'),
    
]