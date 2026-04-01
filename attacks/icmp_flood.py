#!/usr/bin/env python3
"""
ICMP Flood Attack Simulation
- Sends large ping requests (1000 bytes) to localhost
- Creates high-volume ICMP traffic
- Ethical simulation for educational purposes only
"""

import os
import time
import sys

def icmp_flood():
    print("[*] ICMP Flood Attack Simulation")
    print("[*] Target: 127.0.0.1")
    print("[*] Payload size: 1000 bytes")
    print("[*] Press Ctrl+C to stop")
    
    packet_count = 0
    try:
        while True:
            # Windows ping command with 1000-byte payload
            os.system("ping -n 1 -l 1000 127.0.0.1 > nul 2>&1")
            packet_count += 1
            if packet_count % 100 == 0:
                print(f"[+] Sent {packet_count} ICMP packets", end='\r')
            time.sleep(0.01)  # Prevent system overload
    except KeyboardInterrupt:
        print(f"\n[*] ICMP Flood stopped. Total packets: {packet_count}")
        sys.exit(0)

if __name__ == "__main__":
    icmp_flood()