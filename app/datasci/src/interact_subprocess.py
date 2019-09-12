# Non-blocking interaction with a socket server child process, using a thread
# and a queue.
#
# Tested with Python 3.6
#
# Eli Bendersky [http://eli.thegreenplace.net]
# This code is in the public domain.
import queue
import socket
import subprocess
import threading
import time
import sys
import os
import signal

def socket_reader(sockobj, outq, exit_event):
    """Reads from sockobj, 1 byte at a time; places results in outq.
    This function runs in a loop until the sockobj connection is closed or until
    exit_event is set.
    """
    while not exit_event.is_set():
        try:
            buf = sockobj.recv(1)
            if len(buf) < 1:
                break
            outq.put(buf)
        except socket.timeout:
            continue
        except OSError as e:
            break
    
def run(command):   
    sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        sockobj.connect(('localhost', 5000))
    except Exception as e:        
        return e
        
    try:      
        sockobj.send(command.encode())
        out = sockobj.recv(1)
        return out
    except Exception as e:        
        return e
        
    sockobj.close()