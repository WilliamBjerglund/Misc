import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
SERVER_TCP_PORT = 8888  # Port for further communication (e.g., file transfer)

# Get the server's IP address (simplistic approach; may need adjustment for complex setups)
server_ip = socket.gethostbyname(socket.gethostname())

# Prepare the multicast discovery message in the format "SERVER:<server_ip>:<tcp_port>"
message = f"SERVER:{server_ip}:{SERVER_TCP_PORT}"
message_bytes = message.encode('utf-8')

# Create a UDP socket for multicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# Set multicast TTL to allow the message to travel within the local network
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

# Send the discovery message to the multicast group
sock.sendto(message_bytes, (MCAST_GRP, MCAST_PORT))
print("Server discovery message sent:", message)