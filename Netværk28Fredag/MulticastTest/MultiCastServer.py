import socket
import struct

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
SERVER_TCP_PORT = 8888  # Port for further communication


server_ip = socket.gethostbyname(socket.gethostname())

# Prepare the multicast discovery message: "SERVER:<server_ip>:<tcp_port>"
message = f"SERVER:{server_ip}:{SERVER_TCP_PORT}"
message_bytes = message.encode('utf-8')

# Create a UDP socket for multicast (both sending and receiving)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

# Bind to the multicast port so we can receive responses
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sL", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# Send the server discovery message to the multicast group
sock.sendto(message_bytes, (MCAST_GRP, MCAST_PORT))
print("Server discovery message sent:", message)

# Wait for client responses (for a limited time)
print("Waiting for client responses...")
sock.settimeout(5)  # Wait up to 5 seconds for client responses
try:
    while True:
        data, addr = sock.recvfrom(1024)
        msg = data.decode('utf-8')
        if msg.startswith("CLIENT:"):
            try:
                tag, client_ip, client_port = msg.split(":")
                client_port = int(client_port)
                print(f"Discovered client at IP {client_ip} with port {client_port}")
            except ValueError:
                print("Malformed client message:", msg)
except socket.timeout:
    print("No more client responses received.")

sock.close()
