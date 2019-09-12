# first of all import the socket library 
import os
import socket                
import sys
from subprocess import Popen, PIPE, STDOUT
import signal
import threading
import time

# next create a socket object 
class SocketStreamOutput:
    def __init__(self):                                        
        self.process = Popen(["python3","-i","-q","-u"],  # start the process
                                stdin=PIPE,  # pipe its STDIN so we can write to it
                                stdout=PIPE,  # pipe its STDIN so we can process it
                                stderr=PIPE,
                                universal_newlines=True)
        self.output_buffer = sys.stdout  # a buffer to write rasa's output to
        self.input_buffer = sys.stdin
        self.error_buffer = sys.stderr
        
    def run_server(self, host, port):
        s = socket.socket()          
        print("Socket successfully created")
          
        # reserve a port on your computer in our 
        # case it is 12345 but it can be anything 
          
        # Next bind to the port 
        # we have not typed any ip in the ip field 
        # instead we have inputted an empty string 
        # this makes the server listen to requests  
        # coming from other computers on the network 
        # s.bind(('127.0.0.1', 5000))
        s.bind((host, port))
        print("socket binded to %s" %(port) )

        # put the socket into listening mode 
        s.listen(5)
        print("socket is listening")
        c, addr = s.accept()
        
        while True:    
            # Establish connection with client.    
            print('Got connection from', addr)

            data = c.recv(1024)
            if not data:
                pass
            else :
                cmd = data
                output = self.run([b'1+1\n', b'2+2\n'])
                c.send(output)
                # print(output)
                # print(cmd)
                
        c.close()

    def print_buffer(self, timer, wait, buffer_in, buffer_out, buffer_target, buffer_err):
        return True
        for cmd in buffer_in:
            print(cmd, file=buffer_out, flush=True)
            print(self.input_buffer.readline(), file=buffer_target, flush=True)

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
        
        # now we'll read the `rasa` STDOUT line by line, forward it to output_buffer and reset
        '''
        output = []
        for line in self.process.stdout.read():
            output.append(line)
        return output
        '''
        '''
        output = []
        for line in self.process.stdout:
            output.append(line)
        '''
        
        output 
        
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait(timeout=0.2)
    
        return b"test"

    def finished(self):
        self.socker.close()

if __name__ == "__main__":
    s = SocketStreamOutput()
    s.run_server('localhost', 5000)

