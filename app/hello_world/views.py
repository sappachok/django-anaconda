import os
from django.shortcuts import render
from django.views.generic import TemplateView
import pandas as pd
# from hello_world.templatetags import current_tags

from django import template

register = template.Library()

import matplotlib.pyplot as plt
# %matplotlib inline

app_dir = os.path.abspath(os.path.dirname(__file__))
# df = pd.read_excel('data_sheets/titanic.xls')

# df = pd.read_csv('D:/github-repo/django-datasci/app/hello_world/data_sheets/titanic.csv')

# Create your views here.
def hello_world(request):
    path = app_dir
    debug = ''
    df = pd.read_csv(os.path.join(app_dir, 'data_sheets','titanic.csv'))
    data = {'blog_title':'my first app', 'person':df, 'path':path, 'debug':debug, 'listview': ''}
    return render(request, 'hello_world.html', data)

class AboutView(TemplateView):
    template_name = "about.html"