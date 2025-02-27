"""
SimpleUDPServer.py

This script listens for incoming UDP datagrams on a specified port.
Changes from the original:
- After receiving a message, the server sends a reply back to the client's address.
- The reply is a simple acknowledgement message indicating that the server received the message.
"""

from socket import *

HOST = ''           # Listen on all available interfaces
PORT = 9999         # Non-privileged port
CONN_COUNTER = 0    # Counter for connections
BUFFER_SIZE = 1024  # Receive buffer size

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))    # Bind socket to the address
print('UDP server running...')
print('Listening for incoming connections on port ' + str(PORT))

while True:
    CONN_COUNTER += 1
    data, client_address = s.recvfrom(BUFFER_SIZE)
    print('* Connection {} received from {}'.format(CONN_COUNTER, client_address))
    print('\tIncoming text:', data.decode('utf-8'))
    
    # Prepare and send a reply back to the client
    reply_message = "Server received your message"
    s.sendto(reply_message.encode('utf-8'), client_address)