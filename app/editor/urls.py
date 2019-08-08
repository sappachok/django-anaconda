from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from editor.views import BasicSampleFormView
from django.urls import reverse

urlpatterns = [
    url('', TemplateView.as_view(
        template_name="view.html"
    ), name='editor'),
    url('/form/$', BasicSampleFormView.as_view(
        template_name="form.html"
    ), name='codemirror-form'),
]