import os
from django.shortcuts import render
import pandas as pd

import matplotlib.pyplot as plt
# %matplotlib inline

df = pd.read_excel('data_sheets/UOC_STAFF.xls')


# Create your views here.
def hello_world(request):
    path = os.path.abspath(os.path.dirname(__file__))
    content = {'blog_title':'my first app', 'person':df, 'path':path}
    return render(request, 'hello_world.html', content)
