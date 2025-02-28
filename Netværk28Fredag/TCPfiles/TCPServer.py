# TCPServer.py
"""
TCPServer.py

This script implements a TCP server that receives a file from a client.
It performs the following:
- Receives file data in binary mode in chunks (BUFFER_SIZE=1024).
- Writes the incoming data to a uniquely named file ("received_file_{CONN_COUNTER}").
- Sends a confirmation message back to the client once the complete file is received.
"""

from socket import *

HOST = ''           # Listen on all available interfaces.
PORT = 8888         # Non-privileged port.
CONN_COUNTER = 0    # Connection counter.
BUFFER_SIZE = 1024  # Buffer size for receiving data.

# Create a TCP socket, bind it, and start listening for connections.
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print('* TCP Server listening for incoming connections on port {}'.format(PORT))

while True:
    CONN_COUNTER += 1
    conn, addr = server_socket.accept()
    print('* Connection {} received from {}'.format(CONN_COUNTER, addr))
    
    # Create a uniquely named file to store the incoming data.
    filename = "received_file_{}".format(CONN_COUNTER)
    with open(filename, "wb") as file:
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            file.write(data)
    
    print("File received and saved as '{}'.".format(filename))
    
    # Send a confirmation message back to the client.
    confirmation = "File received successfully"
    conn.send(confirmation.encode('utf-8'))
    
    conn.close()
