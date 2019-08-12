import os
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.management.base import BaseCommand
from django.http import HttpResponse

from sys import stdout, stdin, stderr
from myproc import ProcessManager

import requests
import json
from html.parser import HTMLParser
import psycopg2

app_dir = os.path.abspath(os.path.dirname(__file__))

command = [
    "a = 1",
    "b = 2",
    "c = a+b",
    "print(c)",
]

print(command)
pm = ProcessManager()
pm.set_process(["python","../../manage.py", "shell"])