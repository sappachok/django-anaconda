from django.http import JsonResponse
import sys
import json
import io
import sys
import os
import matplotlib.pyplot as plt
import urllib, base64
import numpy as np
import pandas as pd

output = []
def hello():
    output.append({"type":"html", "value":"Hello!!"})
    return output

def get_type(obj):

    return output

def print_header(text):
    output.append({"type":"html", "value":"<h1>" + str(text) + "</h1>"})
    return output

def print_text(text):
    output.append({"type":"html", "value":text})
    return output

def print_code(text):
    output.append({"type":"code", "value":text})
    return output

def print_buffer(temp):
    buffer = io.StringIO()
    s = buffer.getvalue()
    output.append({"type":"code", "value":s})
    return output

def print_type(obj):
    output.append({"type":"html", "value":type(obj)})
    return output

def print_table(obj):
    if(get_type(obj)=="pandas.core.frame.DataFrame"):
        output.append({"type":"html", "value":obj.to_html()})
    else:
        pass

    return output

def print_html(html):
    output.append({"type":"html", "value":html})
    return output

def show_pyplot(plt):
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    output.append({"type":"image", "value":"<img src='" + uri + "'>"})
    return output

def print_output():
    print(json.dumps(output, separators=(',', ':')))

def print_error(err_msg):
    print(json.dumps({"type":"error", "value":err_msg}, separators=(',', ':')))