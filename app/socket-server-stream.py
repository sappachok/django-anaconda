#!/usr/bin/env python

import socket
import select
import socketserver
import os
import sys
from subprocess import Popen, PIPE, STDOUT
import threading
import time


class SocketServer:
    """ Simple socket server that listens to one single client. """

    def __init__(self, host = '0.0.0.0', port = 2010):
        """ Initialize the server with a host and port to listen to. """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(1)
        
        self.input_buffer = sys.stdin
        self.output_buffer = sys.stdout  # a buffer to write rasa's output to
        self.error_buffer = sys.stderr
        
        self.process = Popen(["python3","-i","-q","-u"],  # start the process
                                stdin=PIPE,  # pipe its STDIN so we can write to it
                                stdout=self.output_buffer,  # pipe its STDIN so we can process it
                                stderr=self.output_buffer,
                                universal_newlines=True)        

    def close(self):
        """ Close the server socket. """
        print('Closing server socket (host {}, port {})'.format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None

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

    def run_server(self):
        """ Accept and handle an incoming connection. """
        print('Starting socket server (host {}, port {})'.format(self.host, self.port))

        client_sock, client_addr = self.sock.accept()

        print('Client {} connected'.format(client_addr))

        stop = False
        while not stop:
            if client_sock:
                # Check if the client is still connected and if data is available:
                try:
                    rdy_read, rdy_write, sock_err = select.select([client_sock,], [], [])
                except select.error:
                    print('Select() failed on socket with {}'.format(client_addr))
                    return 1

                if len(rdy_read) > 0:
                    read_data = client_sock.recv(255)
                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('{} closed the socket.'.format(client_addr))
                        stop = True
                    else:
                        self.run([read_data])
                        #print(read_data.rstrip())
                        if read_data.rstrip() == 'quit':
                            stop = True
                        '''
                        else:
                            client_sock.send(read_data)
                        '''
            else:
                print("No client is connected, SocketServer can't receive data")
                stop = True

        # Close socket
        print('Closing connection with {}'.format(client_addr))
        client_sock.close()
        self.process.stdin.close()
        self.process.terminate()
        self.process.wait(timeout=0.2)        
        return 0

def main():
    server = SocketServer('localhost', 5000)
    server.run_server()
    print('Exiting')

if __name__ == "__main__":
    main()
