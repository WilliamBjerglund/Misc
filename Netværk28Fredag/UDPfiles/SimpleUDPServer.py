# SimpleUDPServer.py
"""
SimpleUDPServer.py

This script listens for incoming UDP datagrams on a specified port.
It performs the following:
- Checks for offending words in the incoming message and replaces them with "beep".
- Converts the (filtered) message to uppercase.
- Sends the transformed message back to the client.
"""

import re
from socket import *

HOST = ''           # Listen on all available interfaces
PORT = 9999         # Non-privileged port
BUFFER_SIZE = 1024  # Receive buffer size

# List of offending words to filter (example words)
offending_words = ["badword", "offensive"]

def filter_text(text):
    """Replace each offending word with 'beep' (case-insensitive)."""
    for word in offending_words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub("beep", text)
    return text

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))    # Bind socket to the address
print('UDP server running...')
print('Listening for incoming connections on port ' + str(PORT))

while True:
    data, client_address = s.recvfrom(BUFFER_SIZE)
    original_text = data.decode('utf-8')
    print(f'Received from {client_address}: {original_text}')
    
    # Filter the text for offending words
    filtered_text = filter_text(original_text)
    
    # Convert to uppercase for the reply
    reply_message = filtered_text.upper()
    
    # Send reply back to client
    s.sendto(reply_message.encode('utf-8'), client_address)
    print(f'Sent reply: {reply_message} to {client_address}\n')
