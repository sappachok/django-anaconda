# Import socket module 
import socket                
  
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