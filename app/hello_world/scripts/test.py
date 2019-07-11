import io
import os
import sys
import datetime
import web_html
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib, base64
# io.IOBase.flush()
# sys.stdout.flush()
# sys.stdout.buffer.flush()

try:
    app_dir = os.path.abspath(os.path.dirname(__file__))
    time=datetime.datetime.now()
    #output=[]
    #output.append("Current time is %s" % (time))
    #output.append("It 's awesome !!!!")
    #output.append(web_output.hello())
    web_html.print_header("Head Topic")
    web_html.hello()

    numPts = 50
    x = [random.random() for n in range(numPts)]
    y = [random.random() for n in range(numPts)]
    sz = 2 ** (10 * np.random.rand(numPts))

    plt.scatter(x, y, s=sz, alpha=0.5)

    web_html.show_pyplot(plt)

    df = pd.read_csv(os.path.join('/src/hello_world', 'data_sheets','titanic.csv'))
    # df = os.path.join('/src/hello_world', 'data_sheets','titanic.csv')
    # web_html.print_table(df.head())
    web_html.print_text(df.shape)
    # web_html.print_html("<table border=\"1\">\n<tr style=\"align:right;\">\n<td>a</td></tr></table>\n")
    # web_html.print_html(df.info())
    # type(df.info())

    # web_html.print_buffer(df.info(buf=buffer))
    # web_html.get_type(df.info())
    #web_html.print_table(df.info(verbose=False))
    web_html.print_output()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    web_html.print_error("Err: {}, File: {}, Line: {}".format(exc_type, fname, exc_tb.tb_lineno))

#print(output)