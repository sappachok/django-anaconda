import os
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.management.base import BaseCommand
from django.http import HttpResponse

from sys import stdout, stdin, stderr
from subprocess import Popen, PIPE, STDOUT, check_output

import requests
import json
from html.parser import HTMLParser
import psycopg2

app_dir = os.path.abspath(os.path.dirname(__file__))

connection = psycopg2.connect(user="postgres",
                                           password="postgres",
                                           host="db",
                                           port="5432",
                                           database="postgres")

# Create your views here.
def datasci(request):
    # db_output = connectdb()
    db_output = []
    template_dir = 'http://localhost:8000/static/templates/admin-lte'
    data = {'blog_title': 'Datasci App', 'get_project_url': 'getproject', 'template_dir': template_dir}
    return render(request, 'index.html', data)

def project(request, pid):
    # db_output = connectdb()
    # output = []
    project_info = get_project_info(pid)
    output = Command(["python", os.path.join(app_dir, "runscript.py"), pid])
    # output.append(test)
    # command = "print('test')"
    # process = Popen(command, stdout=PIPE, stderr=STDOUT)
    # db_output.append(process.stdout.read())
    # parser = HTMLParser()
    # parser.feed(output)

    if output["result"] == True:
        output_print = output["output"][0]
        output_list = output["output"][1]
        error = ""
    else:
        output_print = ""
        output_list = ""
        error = output["error"]

    data = {'blog_title': 'Datasci App', 'project_info': project_info, 'error': error, 'output_print': output_print, 'output_list': output_list}
    # pretty_data = db_output
    # return HttpResponse(pretty_data, content_type="application/json")
    return render(request, 'view-data.html', data)

def get_project_info(pid):
    try:
        cursor = connection.cursor()
        select = """SELECT name, title, description FROM editor_pythonlab WHERE name='{0}'""".format(pid)
        cursor.execute(select)
        record = cursor.fetchone()
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL : {0}" + format(error))

def Command(cmd):
    command = cmd
    try:
        process = Popen(command, stdout=PIPE, stderr=STDOUT, encoding="utf-8")
        tmp = process.stdout.read()
        exoutput = tmp.split('### OUTPUT ###')

        if len(exoutput) > 1:
            output = [exoutput[0], json.loads(exoutput[1])]
        else:
            output = tmp

        exitstatus = process.poll()

        if (exitstatus == 0):
            return {"result": True, "output": output}
        else:
            return {"result": False, "error": tmp, "output": ''}
    except Exception as e:
        return {'result':False, 'error': str(e)}

class OBufferParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag == "!output":
            self.output = ""

    def handle_endtag(self, tag):
        if tag == "!output":
            self.output = ""

    def handle_data(self, data):
            self.output = data

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

class SampleView(TemplateView):
    template_name = 'about.html'
