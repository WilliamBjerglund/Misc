import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
CLIENT_TCP_PORT = 9999  # Port where the client can accept further connections

# Create a UDP socket for multicast (for both receiving and sending)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # Bind to the multicast port
mreq = struct.pack("4sL", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Waiting for server discovery message...")

# Receive the server's discovery message
data, addr = sock.recvfrom(1024)
message = data.decode('utf-8')
print("Received discovery message:", message)

# Parse the server message (expected format: "SERVER:<server_ip>:<tcp_port>")
try:
    tag, server_ip, server_port = message.split(":")
    server_port = int(server_port)
    if tag == "SERVER":
        print(f"Discovered server at IP {server_ip} with TCP port {server_port}")
except ValueError:
    print("Received malformed server discovery message.")

# Determine the client's IP address
client_ip = socket.gethostbyname(socket.gethostname())

# Prepare and send the client response: "CLIENT:<client_ip>:<client_tcp_port>"
client_message = f"CLIENT:{client_ip}:{CLIENT_TCP_PORT}"
sock.sendto(client_message.encode('utf-8'), (MCAST_GRP, MCAST_PORT))
print("Sent client response message:", client_message)

sock.close()
