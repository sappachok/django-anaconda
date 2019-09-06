# first of all import the socket library 
import socket                
from sys import stdout, stdin, stderr
from subprocess import Popen, PIPE, STDOUT, check_output, CalledProcessError

# next create a socket object 
s = socket.socket()          
print("Socket successfully created")
  
# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 5000                
  
# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests  
# coming from other computers on the network 
s.bind(('127.0.0.1', port))         
print("socket binded to %s" %(port) )

# put the socket into listening mode 
s.listen(5)      
print("socket is listening")

proc = Popen(['python3', '-i'],
                stdin=PIPE, 
                stdout=PIPE,
                stderr=PIPE
                )
                
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
    # Establish connection with client. 
    c, addr = s.accept()      
    print('Got connection from', addr )

    data = c.recv(1024)
    if not data:
        break
    else :
        cmd = data
        try :
            proc.stdin.write(cmd)
            proc.stdin.flush()
            #print("...")
            #c.send(cmd)
            print(cmd)
            c.send(proc.stdout.readline())
        except Exception as e:
            print('Error : {0}'.format(e))

 
    # c.send(b'Thank you for connecting') 

    # Close the connection with the client 
    c.close()
    
s.close()