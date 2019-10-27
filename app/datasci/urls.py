from django.urls import path
from datasci.views import SampleView
from datasci import views

from django.conf.urls import include, url
from django.views.generic.base import TemplateView

urlpatterns = [
    path('/', views.datasci, name='datasci'),

    path('/dashboard/', views.dashboard, name='dashboard'),
    path('/dashboard/sample', views.dashboard_sample, name='dashboard-sample'),

    path('/project/<str:pid>/', views.project_ex, name='project'),
    path('/project_ex/<str:pid>/', views.project_ex2, name='project-ex'),
    path('/project_preview/<str:pid>/', views.project_preview, name='project-preview'),
    path('/project_session_clear/<str:pid>/', views.project_session_clear, name='project-session-clear'),

    path('/chart_editor_list', views.chart_editor_list, name='chart-editor-list'),
    path('/chart_editor/', views.chart_editor, name='chart-editor'),
    path('/chart_editor/<str:pid>', views.chart_editor, name='chart-editor'),
    path('/chart_editor_process/', views.chart_editor_process, name='chart-editor-process'),
    path('/chart_editor_preview/', views.chart_editor_preview, name='chart-editor-preview'),
    path('/chart_editor_preview/<str:pid>', views.chart_editor_preview, name='chart-editor-preview'),
    path('/chart_dataset/', views.chart_dataset, name='chart-dataset'),
    path('/chart_dataset/<str:pid>', views.chart_dataset, name='chart-dataset'),


    path('/editor/<str:pid>/', views.editor, name='editor'),
    path('/editor_runresponse/<str:pid>/', views.editor_runresponse, name='editor-runresponse'),
    path('/editor_process/', views.editor_process, name='editor-process'),

    path('/get-output/', views.get_interactive_output, name='get-output'),
    path('/chartjs/', views.chartjs, name='chartjs'),
    path('/chartjs/api/', views.chart_data, name='chartjs-chart_data'),
    path('/about/', SampleView.as_view(), name='about'),
    path('/kill_process/<int:pid>/', views.kill_process, name='kill-process'),
    
]