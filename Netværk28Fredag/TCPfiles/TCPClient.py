# TCPClient.py
"""
TCPClient.py

This script implements a TCP client that sends a .pdf file (or any file) to a server.
It:
- Prompts the user for the file path (or uses a command-line argument).
- Reads the file in binary mode in chunks (BUFFER_SIZE=1024) and sends it.
- Shuts down the sending side to indicate the file is completely sent.
- Optionally waits for and prints a confirmation message from the server.
"""

from socket import *
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8888
BUFFER_SIZE = 1024

# Get the file path from the command line or prompt the user.
if len(sys.argv) < 2:
    FILE_TO_SEND = input("Enter the file path to send: ")
else:
    FILE_TO_SEND = sys.argv[1]

# Create a TCP socket and connect to the server.
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

try:
    with open(FILE_TO_SEND, "rb") as file:
        while True:
            chunk = file.read(BUFFER_SIZE)
            if not chunk:
                break
            client_socket.sendall(chunk)
except FileNotFoundError:
    print(f"File not found: {FILE_TO_SEND}")
    client_socket.close()
    sys.exit(1)

# Signal that the file has been completely sent.
client_socket.shutdown(SHUT_WR)
print("File sent.")

# Optionally, receive a confirmation message from the server.
data = client_socket.recv(BUFFER_SIZE)
print("Received from server:", data.decode('utf-8'))

client_socket.close()
