import os
from django.shortcuts import render
from django.views.generic import TemplateView
import requests
import sys
from subprocess import run,PIPE
import io
import urllib, base64
import json
#from StringIO import StringIO

import random
import pandas as pd
import numpy as np

import psycopg2
# from hello_world.templatetags import current_tags

import matplotlib.pyplot as plt
# %matplotlib inline

app_dir = os.path.abspath(os.path.dirname(__file__))
# Create your views here.

def testscript(request):
    result = ""
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="db",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        print(connection.get_dsn_parameters(), "\n")
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    data = {'info': ''}
    return render(request, 'script.html', data)

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
    arr_output = []
    arr_output.append(setImage(setPlt()))
    data = {'blog_title': 'my first app', 'person': df, 'path': path, 'debug': debug, 'listview': '', 'arr_output': arr_output}
    return render(request, 'hello_world.html', data)

def call_pot(request):
    out = run([sys.executable,'/src/hello_world/scripts/pot.py'],shell=False,stdout=PIPE).stdout.decode('utf-8')
    print(out)

    return render(request, 'pot.html', {'data':out})

def call_func(request):
    inp = 'sappachok'
    output = run([sys.executable,'/src/hello_world/scripts/test.py', inp],shell=False,stdout=PIPE).stdout.decode('utf-8')
    arr_output = []
    try:
        arr_output = json.loads(output)
    except:
        arr_output.append("script has error!!")

    return render(request, 'output.html', {'output':arr_output})

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
    image = {'type':'image', 'src': imagedata}
    return image

def load_file(path):
    f = open(path, "r")
    contents =f.read()
    return contents

class AboutView(TemplateView):
    template_name = "about.html"