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
    
def main():   
    proc = subprocess.Popen(['python3', '-u', 'socket-server.py'])
    time.sleep(0.2)
    
    try:
        while True:
            sockobj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sockobj.settimeout(0.1)
            sockobj.connect(('localhost', 5000))
            outq = queue.Queue()
            exit = threading.Event()
            t = threading.Thread(target=socket_reader, args=(sockobj, outq, exit))
            t.start()
            time.sleep(0.2)
            
            command = input()
            sockobj.send(command.encode())
            
            # Drain the read queue until it's empty; we could've blocked here
            # instead, but this is just for demonstration.
            while True:
                try:
                    v = outq.get(block=False)
                    print(v)
                except queue.Empty:
                    break
 
            if command == "quit()":
                break
                
    finally:
        sockobj.send(b'quit()')
        sockobj.close()
        exit.set()
        proc.terminate()
        
        try:
            proc.wait(timeout=0.2)
            print('== subprocess exited with rc =', proc.returncode)
        except subprocess.TimeoutExpired:
            print('subprocess did not terminate in time')
            
        t.join()
        return False

if __name__ == '__main__':
    main()