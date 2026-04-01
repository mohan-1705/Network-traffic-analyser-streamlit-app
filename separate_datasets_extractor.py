#!/usr/bin/env python3
from scapy.all import rdpcap, IP, TCP, UDP, ICMP
import pandas as pd
import os

def extract_features(pcap_file):
    packets = rdpcap(pcap_file)
    features = []
    for pkt in packets:
        if IP not in pkt:
            continue
        ip = pkt[IP]
        row = {
            'timestamp': float(pkt.time),
            'src_ip': ip.src,
            'dst_ip': ip.dst,
            'length': ip.len,  # IP payload length (excludes link-layer)
            'protocol_type': 0,
            'syn_flag': 0,
            'ack_flag': 0,
            'icmp_payload_size': 0,
            'dst_port': 0,
            'is_http_traffic': 0,
            'is_partial_http': 0
        }
        
        if TCP in pkt:
            tcp = pkt[TCP]
            row['protocol_type'] = 1
            row['syn_flag'] = 1 if (tcp.flags & 0x02) else 0
            row['ack_flag'] = 1 if (tcp.flags & 0x10) else 0
            row['dst_port'] = int(tcp.dport)
            
            # Analyze HTTP traffic on ports 80, 8000, 8080 (non-SYN packets only)
            if tcp.dport in [80, 8000, 8080] and not (tcp.flags & 0x02):
                try:
                    payload = bytes(tcp.payload)
                    if len(payload) > 0:
                        # Check if it looks like an HTTP request
                        payload_str = payload.decode('utf-8', errors='ignore')
                        if payload_str.startswith(('GET ', 'POST ', 'HEAD ', 'PUT ')):
                            row['is_http_traffic'] = 1
                            # 🔑 Critical: Check for incomplete HTTP request (Slowloris signature)
                            if b'\r\n\r\n' not in payload:
                                row['is_partial_http'] = 1
                        # Also mark continuation headers (like "X-Slowloris: ...") as HTTP if port matches
                        elif any(hdr in payload_str for hdr in ['X-', 'User-Agent:', 'Accept:', 'Host:']):
                            row['is_http_traffic'] = 1
                            if b'\r\n\r\n' not in payload:
                                row['is_partial_http'] = 1
                except:
                    # If decoding fails, conservatively assume partial if port is HTTP
                    if tcp.dport in [80, 8000, 8080]:
                        row['is_http_traffic'] = 1
                        row['is_partial_http'] = 1
        
        elif UDP in pkt:
            row['protocol_type'] = 2
            row['dst_port'] = int(pkt[UDP].dport)
        
        elif ICMP in pkt:
            row['protocol_type'] = 3
            if hasattr(pkt[ICMP], 'payload'):
                row['icmp_payload_size'] = len(pkt[ICMP].payload)
        
        features.append(row)
    return features

def main():
    CAPTURES_DIR = r'C:\Users\cheku\OneDrive\Documents\network_dataset\captures'
    OUTPUT_DIR = r'C:\Users\cheku\OneDrive\Documents\network_dataset'
    
    for filename in os.listdir(CAPTURES_DIR):
        if not filename.endswith('.pcapng'):
            continue
        base = filename.replace('.pcapng', '')
        out_csv = os.path.join(OUTPUT_DIR, f"{base}.csv")
        pcap_path = os.path.join(CAPTURES_DIR, filename)
        
        print(f"[+] Processing {filename}")
        feats = extract_features(pcap_path)
        if feats:
            df = pd.DataFrame(feats)
            # Ensure all expected columns exist
            expected_cols = ['timestamp', 'src_ip', 'dst_ip', 'length', 'protocol_type',
                           'syn_flag', 'ack_flag', 'icmp_payload_size', 'dst_port',
                           'is_http_traffic', 'is_partial_http']
            for col in expected_cols:
                if col not in df.columns:
                    df[col] = 0
            df.to_csv(out_csv, index=False)
            print(f"    → Saved {len(feats)} packets to {out_csv}")

if __name__ == "__main__":
    main()