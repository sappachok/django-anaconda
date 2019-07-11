import os
from django.shortcuts import render
from django.views.generic import TemplateView
import requests
import sys
from subprocess import run,PIPE
import io
import urllib, base64

import random
import pandas as pd
import numpy as np
# from hello_world.templatetags import current_tags

import matplotlib.pyplot as plt
# %matplotlib inline

app_dir = os.path.abspath(os.path.dirname(__file__))
# Create your views here.

def run_script():
    tmp_output = ''
    script = load_file("/src/hello_world/scripts/test.py")
    eval('tmp_output = exec("{}")'.format(script))
    return tmp_output

def hello_world(request):
    path = app_dir
    debug = ''
    df = pd.read_csv(os.path.join(app_dir, 'data_sheets','titanic.csv'))

    imageurl = setPlt()

    output = []
    output.append(setImage(setPlt()))

    script = load_file("/src/hello_world/scripts/test.py")

    text = "" #exec(open('/src/hello_world/scripts/test.py').read())
    data = {'blog_title': 'my first app', 'person': df, 'path': path, 'debug': debug, 'listview': '', 'output': output, 'script': text}
    return render(request, 'hello_world.html', data)

def call_pot(request):
    inp = 'sappachok'
    out = run([sys.executable,'/src/hello_world/scripts/pot.py'],shell=False,stdout=PIPE)
    print(out)

    return render(request, 'pot.html', {'data':out.stdout})

def call_func(request):
    inp = 'sappachok'
    out = run([sys.executable,'/src/hello_world/scripts/test.py', inp],shell=False,stdout=PIPE)
    print(out)

    return render(request, 'output.html', {'data':out.stdout})

def setPlt():
    numPts = 50
    x = [random.random() for n in range(numPts)]
    y = [random.random() for n in range(numPts)]
    sz = 2 ** (10*np.random.rand(numPts))

    # plt.figure(figsize=(32, 18))

    plt.scatter(x, y, s=sz, alpha=0.5)

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    return uri

def setImage(imagedata):
    image = { 'type':'image', 'src': imagedata}
    return image

def load_file(path):
    f = open(path, "r")
    contents =f.read()
    return contents

class AboutView(TemplateView):
    template_name = "about.html"