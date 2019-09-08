# Import socket module 
import os
import socket             
from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError
import fcntl
import asyncio
import io

def connect():
    # Create a socket object 
    s = socket.socket()          
      
    # Define the port on which you want to connect 
    port = 5000    
      
    # connect to the server on local computer 
    s.connect(('127.0.0.1', port)) 
      
    # receive data from the server 
    print(s.recv(1024))

    # s.sendall(b'Hello, world')
    
    # close the connection 
    s.close() 

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    proc.stdin.write(b'2+1\n')
    proc.stdin.flush()   
    
    stdout, stderr = await proc.communicate()

    # return f'[{cmd!r} exited with {proc.returncode}]'
    
    data = {
        'stdout' : '',
        'stderr' : ''
    }
    
    if stdout:
        data.stdout = f'[stdout]\n{stdout.decode()}'
        
    if stderr:
        data.stderr = f'[stderr]\n{stderr.decode()}'
        
    return data
    
def test_command():
    

    proc = Popen(['python3', '-i'],
                    stdin=PIPE, 
                    stdout=PIPE, 
                    stderr=PIPE
                    )
   
    data = []
    data.append("start")

    # fcntl.fcntl(proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
    
    try:
        proc.stdin.write(b'2+2\n')
        proc.stdin.flush()        
        open, error = proc.communicate()
        data.append(open.splitlines())
    except Exception as e:
        data.append(e)
        return data

    io_open()
    
    try:
        proc.stdin.write(b'2+1\n')
        proc.stdin.flush()        
        open, error = proc.communicate()
        data.append(open.splitlines())
        #data.append(proc.stdout.read())
    except Exception as e:
        data.append(e)
        return data
        
    proc.terminate()
    proc.wait(timeout=0.1)
    
    return data