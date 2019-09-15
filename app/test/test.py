# Import socket module 
import os
import socket             
from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError
import fcntl
import asyncio
import io
import threading

data = []

def reader(command_list, pipe):
    for f in command_list:
        ln = f
        if not ln: break
        pipe.stdin.write(ln.encode())
        pipe.stdin.flush()
    pipe.stdin.close()
        
proc = Popen(['python3', '-i'], stdin=PIPE, stdout=PIPE)

commands = ['1+1\n','2+2\n','print("hello")\n','import json\n','a=1\n','b=2\n','c=a+b\n','print(c)\n','d=[1,2,3,4]\n','e=json.dumps(d)\n','e']

threads = []
threads.append(threading.Thread(target = reader, args=(commands,proc,)))

for t in threads:
    t.start()

print(proc.stdout.read().splitlines())

print('joining ..')
while threading.active_count() > 1:
    for t in threads:
        t.join()
print('all done.')

proc.terminate()
proc.wait(timeout=0.1)