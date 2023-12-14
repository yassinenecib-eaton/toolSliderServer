#client.py
#!/usr/bin/python3.8

import socket
import time
import signal  

 
# Our signal handler
def signal_handler(signum, frame):  
    print("Signal Number:", signum, " Frame: ", frame)
    print("Signal Number:", signum, " Close socket")
    socket.close(s)
    exit(0)
 
 
# Register our signal handler with `SIGINT`(CTRL + C)
signal.signal(signal.SIGINT, signal_handler)

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

dataClient="Hello I am the client :)"
myint=0
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        myint += 1
        dataClient="Hello I am the client :) " + str(myint)
        s.sendall(dataClient.encode())
        data = s.recv(1024)
        if not data:
            print("No data => close socket and close client")
            socket.close(s)
            break
        print(f"Received {data!r}")
        time.sleep(1)
