# Import socket module 
import os
import socket             
from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError
import fcntl
import asyncio
import io
import threading
'''
proc = Popen(['python3', '-i'],
	    stdin=PIPE, 
	    stdout=PIPE, 
	    stderr=PIPE
	    )
'''

data = []

# fcntl.fcntl(proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

def reader(command_list, pipe):
    for f in command_list:
        ln = f
        if not ln: break
        pipe.stdin.write(ln.encode())
        pipe.stdin.flush()
    pipe.stdin.close()
        
proc = Popen(['python3', '-i'], stdin=PIPE, stdout=PIPE)

commands = ['1+1\n','2+2\n','print("hello")\n','import json\n']

threads = []
threads.append(threading.Thread(target = reader, args=(commands,proc,)))

for t in threads:
    t.start()

'''        
def push_command(cmd):
    try:
        line_cmd = cmd # '{}\r\nprint("############")\r\n'.format(cmd)
        proc.stdin.write(line_cmd.encode())
        proc.stdin.flush()        
        line = proc.stdout.readline()
        return line
    except Exception as e:
        return e

commands = ['1+1\n','2+2\n','print("hello")\n']

for c in commands:
    res = push_command(c)
    data.append(res)
print(data)
'''
print(proc.stdout.read())

print('joining ..')
while threading.active_count() > 1:
    for t in threads:
        t.join()
print('all done.')

proc.terminate()
proc.wait(timeout=0.1)