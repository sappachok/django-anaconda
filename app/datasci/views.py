import os
import signal
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.management.base import BaseCommand
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext

from chartjs.views.lines import BaseLineChartView

from sys import stdout, stdin, stderr
from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError

import requests
import json
from html.parser import HTMLParser
import psycopg2

from io import StringIO
import time
from datasci.src import multicommand, clientsocket, run_multiscript, run_multiscript2, run_multiscript3, interact_subprocess

import fcntl
import select
import time
from datetime import datetime

from editor.models import Invite, PythonCode, PythonLab

app_dir = os.path.abspath(os.path.dirname(__file__))

connection = psycopg2.connect(user="postgres",
                               password="postgres",
                               host="db",
                               port="5432",
                               database="postgres")
# python manage.py shell
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

def project_ex(request, pid):
    project_info = get_project_info(pid)
    project_script = json.loads(project_info[3])
    #script = project_script.split("\n")

    cmd = []

    allcode = []

    cmd.append('from datasci.src import util_interactive')
    cmd.append('_matpotimages_lastoutput = -1')

    for bl in project_script:
        code = []
        script = bl["source"].split("\n")
        type = bl["type"]
        cmd.append("print(\"add_block({})\")\n".format(type))
        for sc in script:
            if sc != '\n':
                code.append(sc)
                allcode.append(sc)
        cmd.append('\n'.join(code))

        cmd.append('_matpotimages = util_interactive.printfigs("fig", None, ".png")')
        cmd.append('if _matpotimages:')
        cmd.append('    for im in _matpotimages:')
        cmd.append('        if im["no"] > _matpotimages_lastoutput:')
        cmd.append('            print(im["src"])')
        cmd.append('            _matpotimages_lastoutput = im["no"]')

        cmd.append("print(\"end_block()\")\n")

    #return HttpResponse("<textarea>{}</textarea>".format(cmd))

    multiscript = run_multiscript.Multiscript()
    output, error = multiscript.run(cmd)


    data = {'blog_title': 'Datasci App', 'project_info': project_info, 'output': output, 'error': error, 'script': '\n'.join(allcode)}
    return render(request, 'view-data-ex.html', data)

def project_session_clear(request, pid):
    fn = 'tmp/session_{}.pkl'.format(pid)
    if os.path.exists(fn):
        os.remove(fn)

    return HttpResponse('Clear session success!!')

def project_preview(request, pid):
    project_info = get_project_info(pid)
    project_script = json.loads(project_info[3])

    cmd = []
    allcode = []

    cmd.append('import os.path')
    cmd.append('import dill')
    cmd.append('import pickle')
    cmd.append('from datasci.src import util_interactive')
    cmd.append('_matpotimages_lastoutput = -1')
    cmd.append("if os.path.isfile('tmp/session_{}.pkl'):".format(pid))
    cmd.append("    dill.load_session('tmp/session_{}.pkl')".format(pid))
    for bl in project_script:
        code = []
        script = bl["source"].split("\n")
        type = bl["type"]
        cmd.append("print(\"add_block({})\")\n".format(type))
        for sc in script:
            if sc != '\n':
                code.append(sc)
                allcode.append(sc)
        cmd.append('\n'.join(code))

        cmd.append('_matpotimages = util_interactive.printfigs("fig", None, ".png")')

        cmd.append('if _matpotimages:')
        cmd.append('    for im in _matpotimages:')
        cmd.append('        if im["no"] > _matpotimages_lastoutput:')
        cmd.append('            print(im["src"])')
        cmd.append('            _matpotimages_lastoutput = im["no"]')

        cmd.append("print(\"end_block()\")\n")

    cmd.append("dill.dump_session('tmp/session_{}.pkl')".format(pid))
    multiscript = run_multiscript.Multiscript()
    output, error = multiscript.run(cmd)

    data = {'blog_title': 'Datasci App', 'project_info': project_info, 'output': output, 'error': error,
            'script': '\n'.join(allcode)}
    return render(request, 'project-preview.html', data)

def project_ex2(request, pid):
    project_info = get_project_info(pid)
    project_script = project_info[3]
    script = project_script.split("\n")

    cmd = []
    code = []

    for sc in script:
        if sc != '\n':
            code.append(sc)

    cmd.append('\n'.join(code))
    cmd.append('from datasci.src import util_interactive')
    cmd.append('util_interactive.printfigs("fig", None, ".png")')
    output, error = run_multiscript2.run(cmd)

    data = {'blog_title': 'Datasci App', 'project_info': project_info, 'output': output, 'error': error,
            'script': '\n'.join(code)}
    return render(request, 'view-data-ex2.html', data)

def get_project_info(pid):
    try:
        cursor = connection.cursor()
        select = """SELECT name, title, description, script FROM editor_pythonlab WHERE name='{0}'""".format(pid)
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

def editor(request, pid=""):
    project_info = get_project_info(pid)
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d%b%Y%H%M%S%f)")
    data = {'blog_title': 'Python Editor', 'project_info': project_info, 'now':timestampStr}
    
    return render(request, 'python-editor.html', data)

def run_interactive_script(pid, script):
    cmd = []
    cmd.append('import os.path')
    cmd.append('import dill')
    cmd.append('import pickle')
    cmd.append('from datasci.src import util_interactive')
    cmd.append("if os.path.isfile('tmp/session_{}.pkl'):".format(pid))
    cmd.append("    dill.load_session('tmp/session_{}.pkl')".format(pid))
    cmd.append('else:')
    cmd.append('    _matpotimages_lastoutput = -1')

    type = "script"
    cmd.append("print(\"add_block({})\")\n".format(type))

    cmd.append(script)

    cmd.append('_matpotimages = util_interactive.printfigs("fig", None, ".png")')
    cmd.append('if _matpotimages:')
    cmd.append('    for im in _matpotimages:')
    cmd.append('        print(im["src"])')
    cmd.append('        _matpotimages_lastoutput = im["no"]')

    # cmd.append('print(_matpotimages_lastoutput)')
    cmd.append("print(\"end_block()\")\n")


    cmd.append("dill.dump_session('tmp/session_{}.pkl')".format(pid))

    multiscript = run_multiscript3.Multiscript()
    output, error = multiscript.run(cmd)

    if error == [[]]:
        error = ""

    data = {'output': output, 'error': error, 'script': script}
    return data


def editor_runresponse(request, pid=""):
    # pid = request.POST.get("pid")
    script = request.POST.get("script")
    output = run_interactive_script(pid, script)

    return render(request, 'editor-response.html', output)
    #return HttpResponse(json.dumps(output))
    #return HttpResponse("success")

def run_command(proc, commands):
    for cmd in commands:
        if cmd :
            try :
                tmp = '{0}\n'.format(cmd)
                proc.stdin.write(tmp.encode())
                proc.stdin.flush()
            except Exception as e:
                return "Error : {0}".format(e)
        else :
            pass
    return proc

def kill_process(request, pid):
    os.kill(pid, signal.SIGTERM)
    return HttpResponse("Kill Process {}".format(pid))

def get_interactive_output(request):
    result = interact_subprocess.run('print("Hello!!")')
    return HttpResponse(result)
    
def editor_process(request):
    pid = request.POST.get("pid")
    cmd = request.POST.get("json_value")
    #commands = prepaire_command(cmd)

    try:
        PythonLab.objects.filter(name=pid).update(script=cmd)
    except Exception as e:
        return HttpResponse("Error : {0}".format(e))

    return HttpResponse(cmd)

def prepaire_command(cmd, sp='\r\n'):
    command_list = cmd.split(sp)
    data = []
    for c in command_list:
        data.append(c)

    return data

def chartjs(request):
    data = {'blog_title': 'Datasci App'}
    # pretty_data = db_output
    # return HttpResponse(pretty_data, content_type="application/json")         
    return render(request, 'chartjs.html', data)

def chart_data(request):
    data = {
        'type': 'bar',
        'data': {
            'labels': ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            'datasets': [{
                'label': '# of Votes',
                'data': [12, 19, 3, 5, 2, 3],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                'borderWidth': 1
            }]
        },
        'options': {
            'scales': {
                'yAxes': [{
                    'ticks': {
                        'beginAtZero': True
                    }
                }]
            }
        }
    }

    return JsonResponse(data)

def chart_data_2(request):
    return True