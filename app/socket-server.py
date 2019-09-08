# Helper for testing.
#
# Eli Bendersky [http://eli.thegreenplace.net]
# This code is in the public domain.
import socketserver
import os
from sys import stdout, stdin, stderr
from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError
import threading
from capturer import CaptureOutput

proc = Popen(['python3', '-i'], stdin=PIPE, stdout=PIPE)
'''
proc = Popen(['python3', '-i'],
                    stdin=PIPE, 
                    stdout=PIPE, 
                    stderr=PIPE
                    )
'''
response = []
lines = []

class MyTCPHandler(socketserver.BaseRequestHandler):
    def reader(self):
        for line in self.process.stdout:
            lines.append(line)
            sys.stdout.write(line)
            
    def handle(self):
        self.process = proc
        self.data = self.request.recv(1024).strip()
        # print("{} wrote:".format(self.client_address[0]))
        # print("pid: {}".format(os.getpid()))
        print('<<< {} \n'.format(self.data))
                    
        if self.data == b'quit()':
            self.kill(os.getpid())
            
        
        try:
            cmd = b''.join([self.data, b'\n'])
            # proc.stdin.write(cmd.encode())
            proc.stdin.write(cmd)
            proc.stdin.flush()
            print(stdout.readline())
            # open, error = proc.communicate()
            # print(open.stdout.readline())
            # print(proc.stdout.readline())
            # print(cmd)
            # print(proc.stdout.readline())         
        except Exception as e:
            print(e)
            # response.append(e)
            
        # proc.wait()
        
        # exec(self.data)
        # self.request.sendall(self.data.upper())
    
    def kill(self, pid):
        os.kill(pid, signal.SIGTERM)

if __name__ == "__main__":
    with socketserver.TCPServer(('localhost', 5000), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()