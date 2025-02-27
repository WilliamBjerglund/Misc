"""
TCPClient.py

This script implements a TCP client that sends any file to a server.
Changes from the original:
- The client now accepts the file path from the user via a command-line argument (or prompts for input).
- It opens the specified file in binary read mode and reads its content in chunks (BUFFER_SIZE = 1024 bytes).
- Each chunk is sent to the server until the end of the file is reached.
- Once done, the client shuts down the sending side of the connection and optionally waits for a confirmation message.
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
s = socket(AF_INET, SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))

try:
    with open(FILE_TO_SEND, "rb") as file:
        while True:
            chunk = file.read(BUFFER_SIZE)
            if not chunk:
                break
            s.sendall(chunk)
except FileNotFoundError:
    print(f"File not found: {FILE_TO_SEND}")
    s.close()
    sys.exit(1)

# Signal that the file has been completely sent.
s.shutdown(SHUT_WR)
print("File sent.")

# Optionally, receive a confirmation message from the server.
data = s.recv(BUFFER_SIZE)
print("Received from server:", data.decode('utf-8'))

s.close()
