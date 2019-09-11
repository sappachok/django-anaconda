# first of all import the socket library 
import os
import socket                
import sys
from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError
import os
import signal

# next create a socket object 
class SocketStreamOutput:
    def __init__(self):                                        
        self.process = Popen(["python3","-i","-q","-u"],  # start the process
                                stdin=PIPE,  # pipe its STDIN so we can write to it
                                stdout=PIPE,  # pipe its STDIN so we can process it
                                stderr=PIPE,
                                universal_newlines=True)
        self.output_buffer = sys.stdout  # a buffer to write rasa's output to
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
        
        while True: 
            c, addr = s.accept()
            # Establish connection with client.    
            print('Got connection from', addr)

            data = c.recv(1024)
            if not data:
                break
            else :
                cmd = data
                c.send(b"Hello Client!!")
                print(data)
                
            c.close()

    def print_buffer(self, timer, wait, buffer_in, buffer_out, buffer_target, buffer_err):
        for cmd in buffer_in:
            #self.process.stdin.write(cmd.decode("utf-8"))
            #self.process.stdin.flush()
            print(cmd.decode("utf-8"), file=buffer_target, flush=True)

    def run(self, commands):
        if not commands:
            return False

        input_buffer = commands  # a buffer to get the user input from

        # lets build a timer which will fire off if we don't reset it
        timer = threading.Event()  # a simple Event timer
        input_thread = threading.Thread(target=self.print_buffer,
                                        args=(timer,  # pass the timer
                                              0.1,  # prompt after one second
                                              input_buffer, output_buffer, self.process.stdin, self.process.stderr))

        input_thread.daemon = True  # no need to keep the input thread blocking...
        input_thread.start()  # start the timer thread
        input_thread.join()
        
        # now we'll read the `rasa` STDOUT line by line, forward it to output_buffer and reset
        '''
        output = self.output_buffer.read()
        return output
        '''
        '''
        output = []
        for line in self.process.stdout.read():
            output.append(line)
        return output
        '''
        '''
        error = []
        for line in self.process.stderr:
            error.append(line)
        '''
        #return (output, error)
    def finished(self):
        self.socker.close()

if __name__ == "__main__":
    s = SocketStreamOutput()
    s.run_server('localhost', 5000)

