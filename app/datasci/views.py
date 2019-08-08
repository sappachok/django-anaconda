import os
from django.shortcuts import render
# from django.views.generic import TemplateView
from django.views.generic.base import TemplateView
import requests
import sys
from subprocess import run,PIPE
import io
import urllib, base64
import json
# from StringIO import StringIO

import random
import pandas as pd
import numpy as np

import psycopg2
# from hello_world.templatetags import current_tags

import matplotlib.pyplot as plt
# %matplotlib inline

app_dir = os.path.abspath(os.path.dirname(__file__))

# Create your views here.
def datasci(request):
    db_output = connectdb()
    data = {'blog_title': 'Datasci App', 'output' : db_output}
    return render(request, 'view-data.html', data)

def connectdb():
    arr_output = []
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="db",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        arr_output.append(connection.get_dsn_parameters())
        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        arr_output.append("You are connected to - {0}".format(record))

        cursor.execute("""SELECT
           *
        FROM
           pg_catalog.pg_tables
        WHERE
           schemaname != 'pg_catalog'
        AND schemaname != 'information_schema'
        """)
        record = cursor.fetchone()
        arr_output.append("Tables - {0}".format(record))
        return arr_output
        # query_python_code()
    except (Exception, psycopg2.Error) as error:
        arr_output.append("Error while connecting to PostgreSQL : {0}" + format(error))
        return arr_output
        # return False

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

def test(request):
    path = app_dir
    debug = ''
    df = pd.read_csv(os.path.join(app_dir, 'data_sheets','titanic.csv'))

    imageurl = setPlt()
    arr_output = []
    arr_output.append(setImage(setPlt()))
    data = {'blog_title': 'my first app', 'person': df, 'path': path, 'debug': debug, 'listview': '', 'arr_output': arr_output}
    return render(request, 'example.html', data)

class SampleView(TemplateView):
    template_name = 'about.html'
