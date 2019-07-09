import os
from django.shortcuts import render
import pandas as pd

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
    content = {'blog_title':'my first app', 'person':df, 'path':path, 'debug':debug}
    return render(request, 'hello_world.html', content)

def print_datalist