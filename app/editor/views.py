from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import SampleForm

class BasicSampleFormView(FormView):
    #template_name = 'form.html'
    template_name = 'widget.html'
    form_class = SampleForm

    def get_success_url(self):
        return reverse('codemirror-form')