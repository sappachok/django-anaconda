import os
from django.shortcuts import render
# from django.views.generic import TemplateView
from django.views.generic.base import TemplateView
from django.core.management.base import BaseCommand
from django.http import HttpResponse

from subprocess import Popen
from sys import stdout, stdin, stderr
import time, os, signal
from subprocess import Popen, PIPE, STDOUT, check_output

import requests
import sys
from subprocess import run,PIPE
import io
import urllib, base64
import json
from django.http import JsonResponse

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
    # db_output = connectdb()
    db_output = []

    data = {'blog_title': 'Datasci App', 'get_project_url': 'getproject'}
    return render(request, 'project.html', data)

def getproject(request, pid):
    # db_output = connectdb()
    # output = []
    output = Command(["python", os.path.join(app_dir, "runscript.py"), pid])
    # output.append(test)
    # command = "print('test')"
    # process = Popen(command, stdout=PIPE, stderr=STDOUT)
    # db_output.append(process.stdout.read())
    data = {'blog_title': 'Datasci App', 'output_list': output}
    # pretty_data = db_output
    # return HttpResponse(pretty_data, content_type="application/json")
    return render(request, 'view-data.html', data)


def Command(cmd):
    command = cmd
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT, encoding="utf-8")
        output = json.loads(process.stdout.read())
        exitstatus = process.poll()

        if (exitstatus == 0):
            return output
        else:
            return false
    except Exception as e:
        return {"status": "failed", "output": str(e)}

'''
class Command(BaseCommand):
    help = 'Run all commands'
    commands = [
        'python test.py',
        'python test.py',
    ]
    output_list = []

    def handle(self, *args, **options):
        proc_list = []
        output_list = []

        for command in self.commands:
            proc = Popen(command, shell=True, stdin=stdin, stdout=stdout, stderr=stderr)
            proc_list.append(proc)
            self.output_list.append(proc.stdout.decode('utf-8'))

        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            for proc in proc_list:
                os.kill(proc.pid, signal.SIGKILL)
'''

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
           editor_pythoncode
        """)
        records = cursor.fetchall()
        for rec in records :
           arr_output.append("Record - {0}".format(rec))

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
