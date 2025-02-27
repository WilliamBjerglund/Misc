"""
TCPServer.py

This script implements a TCP server that receives a file from a client.
Changes from the original:
- Instead of receiving just a text message, the server now receives a file in binary mode.
- The incoming data is written to a uniquely named file ("received_file_{CONN_COUNTER}") in binary write mode.
- Data is read in chunks of BUFFER_SIZE (1024 bytes) until the client finishes sending.
- After receiving the complete file, the server sends a confirmation message back to the client.
"""

from socket import *

HOST = ''           # Listen on all available interfaces.
PORT = 8888         # Non-privileged port.
CONN_COUNTER = 0    # Connection counter.
BUFFER_SIZE = 1024  # Buffer size for receiving data.

# Create a TCP socket, bind it, and start listening for connections.
s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print('* TCP Server listening for incoming connections on port {}'.format(PORT))

while True:
    CONN_COUNTER += 1
    conn, addr = s.accept()
    print('* Connection {} received from {}'.format(CONN_COUNTER, addr))
    
    # Save the incoming file data to a uniquely named file.
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
