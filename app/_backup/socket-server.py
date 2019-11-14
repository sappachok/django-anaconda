# Helper for testing.
#
# Eli Bendersky [http://eli.thegreenplace.net]
# This code is in the public domain.
import socketserver
import os
import sys
from subprocess import Popen, PIPE, STDOUT
import threading
import time

class MyTCPHandler(socketserver.BaseRequestHandler):

    def __init__(self):
        self.input_buffer = sys.stdin
        self.output_buffer = sys.stdout  # a buffer to write rasa's output to
        self.error_buffer = sys.stderr
        
        self.process = Popen(["python3","-i","-q","-u"],  # start the process
                                stdin=PIPE,  # pipe its STDIN so we can write to it
                                stdout=self.output_buffer,  # pipe its STDIN so we can process it
                                # stderr=PIPE,
                                universal_newlines=True)
        return
        
    def setup(self):
        pass
               
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                break
                
            print('<<< {} \n'.format(self.data))
            '''
            try :
                result = self.run([self.data])
            except Exception as e:
                print(e)
            '''
                        
            if self.data == b'quit()':
                self.kill(os.getpid())
    
    def print_buffer(self, timer, wait, buffer_in, buffer_out, buffer_target, buffer_err):
        for cmd in buffer_in:
            print(cmd.decode("utf-8"), file=buffer_target, flush=True)
            print("", file=self.output_buffer, flush=True)
            # print(cmd.decode("utf-8"), file=self.process.stdin, flush=True)
            
            #time.sleep(0.2)

    def run(self, commands):
        if not commands:
            return False

        input_buffer = commands  # a buffer to get the user input from

        # lets build a timer which will fire off if we don't reset it
        timer = threading.Event()  # a simple Event timer
        input_thread = threading.Thread(target=self.print_buffer,
                                        args=(timer,  # pass the timer
                                              0.1,  # prompt after one second
                                              input_buffer, self.output_buffer, self.process.stdin, self.process.stderr))

        input_thread.daemon = True  # no need to keep the input thread blocking...
        input_thread.start()  # start the timer thread
        input_thread.join()
    
    def kill(self, pid):
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait(timeout=0.2)    
        os.kill(pid, signal.SIGTERM)

if __name__ == "__main__":    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(('localhost', 5000), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()