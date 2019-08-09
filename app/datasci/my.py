import random
import io
import urllib, base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
import json
from django.http import JsonResponse

class OutputBuffer:
    def __init__(self):
        self.output_list = []

    def setval(self, content_type, val):
        output = {'type': content_type, 'val': val}
        self.output_list.append(output)

    def setfigure(self, plt):
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        output = 'data:image/png;base64,' + urllib.parse.quote(string)
        self.setval("image", output)

    def val(self):
        print(json.dumps(self.output_list))


op = OutputBuffer()
op.setval("header", "Student Data Report")

numPts = 50
x = [random.random() for n in range(numPts)]
y = [random.random() for n in range(numPts)]
sz = 2 ** (10 * np.random.rand(numPts))

# plt.figure(figsize=(32, 18))

plt.scatter(x, y, s=sz, alpha=0.5)

op.setfigure(plt)
# op.setval("image", output)
op.val()