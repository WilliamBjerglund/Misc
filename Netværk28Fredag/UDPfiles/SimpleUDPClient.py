"""
SimpleUDPClient.py

This script sends a UDP datagram to a server running on a specified IP and port.
Changes from the original:
- After sending a message to the server, the client now waits to receive a reply.
- The received reply is decoded and printed to the console.
"""

from socket import *

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
BUFFER_SIZE = 1024

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Message to send
message = "Hello there. My name is Ignacio"
s.sendto(message.encode('utf-8'), (SERVER_IP, SERVER_PORT))
print("Data sent.")

# Wait for a reply from the server
data, server = s.recvfrom(BUFFER_SIZE)
print("Received from server:", data.decode('utf-8'))