# Import socket module 
import os
import socket             
from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError
import fcntl
import asyncio
import io
import threading
import pty

# master, slave = pty.openpty()

data = []

def reader(command_list, pipe_r, pipe_w):  
    for f in command_list:
        ln = f
        if not ln: break
        pipe_w.write(ln.encode())
        pipe_w.flush()
    pipe_w.close()
    pipe_r.close()
    output = pipe_r.read().splitlines()
    # output = []
    print(output)


out_r, out_w = pty.openpty()
        
proc = Popen(['python3', '-i'], stdin=out_w, stdout=out_w)

commands = ['1+1\n','2+2\n','print("hello")\n','import json\n','a=1\n','b=2\n','c=a+b\n','print(c)\n','d=[1,2,3,4]\n','e=json.dumps(d)\n','e\n']

# stdout = os.fdopen(master)

reader(commands, out_r, out_w)

# commands = ['print("hello")']
# reader(commands, proc)

# print(proc.stdout.read().splitlines())
# print(proc.stdout.read())

#print(proc.stderr)

proc.terminate()
proc.wait(timeout=0.1)