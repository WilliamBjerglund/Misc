# SimpleUDPClient.py
"""
SimpleUDPClient.py

This script sends a UDP datagram to a server running on a specified IP and port.
It takes user input as the message, sends it to the server, and waits for a reply.
If a reply is not received (due to UDP's unreliability), it retries a few times.
"""

from socket import *

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9999
BUFFER_SIZE = 1024
TIMEOUT = 2  # seconds
MAX_RETRIES = 3

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)
s.settimeout(TIMEOUT)

# Get user input for the message
message = input("Enter your message: ")

attempt = 0
while attempt < MAX_RETRIES:
    try:
        # Send the message
        s.sendto(message.encode('utf-8'), (SERVER_IP, SERVER_PORT))
        print("Data sent. Waiting for reply...")
        
        # Wait for a reply from the server
        data, server = s.recvfrom(BUFFER_SIZE)
        reply = data.decode('utf-8')
        print("Received from server:", reply)
        break  # Reply received; exit loop
        
    except timeout:
        attempt += 1
        print(f"Timeout occurred. Retrying ({attempt}/{MAX_RETRIES})...")
else:
    print("No reply received after multiple attempts.")

s.close()
