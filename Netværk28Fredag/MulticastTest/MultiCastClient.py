import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

# Create a UDP socket for multicast
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # Listen on all interfaces on the multicast port

# Construct the multicast membership request
mreq = struct.pack("4sL", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Waiting for multicast discovery message...")

# Listen for a multicast discovery message
data, addr = sock.recvfrom(1024)
message = data.decode('utf-8')
print("Received discovery message:", message)

# Parse the message to extract server details
# Expected format: "SERVER:<server_ip>:<tcp_port>"
try:
    tag, server_ip, tcp_port = message.split(":")
    tcp_port = int(tcp_port)
    if tag == "SERVER":
        print(f"Discovered server at IP {server_ip} with TCP port {tcp_port}")
except ValueError:
    print("Received malformed discovery message.")