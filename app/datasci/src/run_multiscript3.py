import subprocess
import sys
import threading
import time

import matplotlib
import io
import urllib, base64

# we'll be using a separate thread and a timed event to request the user input

class Block_output:
    def __init__(self):
        self.output = []

    def add_result(self, type, result):
        self.output.append({
            "type" : type,
            "data" : result
        })
    def result(self):
        return self.output

#result_output = Block_output()
#error_output = []

class Multiscript():
    def __init__(self):
        self.input_buffer = ""  # a buffer to get the user input from
        self.output_buffer = sys.stdout  # a buffer to write rasa's output to
        self.error_buffer = sys.stderr
        self.proc = subprocess.Popen(["python3","-i","-q","-u"],  # start the process
                                stdin=subprocess.PIPE,  # pipe its STDIN so we can write to it
                                stdout=subprocess.PIPE,  # pipe its STDIN so we can process it
                                stderr=subprocess.PIPE,
                                shell=True,
                                universal_newlines=True)

        self.result_output = Block_output()
        self.error_output = []

    def print_buffer(self, timer, wait, buffer_in, buffer_out, buffer_target, buffer_err):
        for cmd in buffer_in:
            buffer_target.write("{}\n".format(cmd))

        buffer_target.flush()
        #time.sleep(0.1)

    def printfigs(name="fig", size=None, ending=".png"):
        # print("Print Figures")
        images = []

        if len(matplotlib.pyplot.get_fignums()) == 1:
            num = matplotlib.pyplot.get_fignums()[0]
            fig = matplotlib.pyplot.figure(num)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            output = 'data:image/png;base64,' + urllib.parse.quote(string)
            images.append("<img src='{}' class='img-responsive'>".format(output))

        for num in matplotlib.pyplot.get_fignums():
            fig = matplotlib.pyplot.figure(num)
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            output = 'data:image/png;base64,' + urllib.parse.quote(string)
            images.append("<img src='{}' class='img-responsive'>".format(output))

    def clear_output(self):
        pass

    def run(self, commands):
        global num_block

        self.input_buffer = commands

        if not self.input_buffer:
            return False

        # lets build a timer which will fire off if we don't reset it
        timer = threading.Event()  # a simple Event timer
        input_thread = threading.Thread(target=self.print_buffer,
                                        args=(timer,  # pass the timer
                                              0.2,  # prompt after one second
                                              self.input_buffer, self.output_buffer, self.proc.stdin, self.proc.stderr))

        input_thread.daemon = True  # no need to keep the input thread blocking...
        input_thread.start()  # start the timer thread
        input_thread.join()

        self.proc.stdin.close()

        output = []
        type = ""

        for line in self.proc.stdout:

            if line == "add_block(script)\n":
                type = "script"
                output = []
            elif line == "add_block(html)\n":
                type = "html"
                output = []
            elif line == "end_block()\n":
                self.result_output.add_result(type, output)
            else:
                output.append(line)

        #result_output.append(output)
        #result_output.pop(0)

        error = []
        for line in self.proc.stderr:
            error.append(line)

        self.proc.terminate()
        self.proc.wait(timeout=0.2)

        #result_output[num_block] = output
        self.error_output.append(error)

        return (self.result_output.result(), self.error_output)