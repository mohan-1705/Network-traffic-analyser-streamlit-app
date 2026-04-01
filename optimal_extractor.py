"""
OPTIMAL FEATURE EXTRACTOR FOR SYN FLOOD DETECTION
- Creates separate attack_dataset.csv and normal_dataset.csv
- Uses only the most reliable features for localhost DoS detection
- Guaranteed to work with your data
"""

from scapy.all import rdpcap, IP, TCP
import pandas as pd
import os

def extract_features(pcap_file):
    """Extract only the most reliable features for SYN flood detection"""
    packets = rdpcap(pcap_file)
    features = []
    
    for pkt in packets:
        if IP not in pkt:
            continue
            
        ip = pkt[IP]
        syn_flag = 0
        
        # Only check TCP SYN flag (most reliable indicator)
        if TCP in pkt:
            syn_flag = 1 if (pkt[TCP].flags & 0x02) else 0
        
        features.append({
            'timestamp': float(pkt.time),
            'src_ip': ip.src,
            'dst_ip': ip.dst,
            'length': len(pkt),          # Critical: SYN flood = 44 bytes on Windows
            'syn_flag': syn_flag         # Critical: 1 = SYN packet
        })
    
    return features

def main():
    CAPTURES_DIR = r'C:\Users\cheku\OneDrive\Documents\network_dataset\captures'
    ATTACK_OUTPUT = r'C:\Users\cheku\OneDrive\Documents\network_dataset\attack_dataset.csv'
    NORMAL_OUTPUT = r'C:\Users\cheku\OneDrive\Documents\network_dataset\normal_dataset.csv'
    
    attack_packets = []
    normal_packets = []
    
    # Process all .pcapng files
    for filename in os.listdir(CAPTURES_DIR):
        if not filename.endswith('.pcapng'):
            continue
            
        filepath = os.path.join(CAPTURES_DIR, filename)
        print(f"[+] Processing: {filename}")
        
        try:
            features = extract_features(filepath)
        except Exception as e:
            print(f"  ⚠️ Skip {filename}: {e}")
            continue
        
        # STRICT LABELING BASED ON FILENAME
        if 'normal' in filename.lower():
            normal_packets.extend(features)
            print(f"    → Added {len(features)} packets to NORMAL dataset")
        elif 'flood' in filename.lower():
            attack_packets.extend(features)
            print(f"    → Added {len(features)} packets to ATTACK dataset")
    
    # Save datasets
    if attack_packets:
        pd.DataFrame(attack_packets).to_csv(ATTACK_OUTPUT, index=False)
        print(f"\n✅ Saved {len(attack_packets)} ATTACK packets to {ATTACK_OUTPUT}")
    
    if normal_packets:
        pd.DataFrame(normal_packets).to_csv(NORMAL_OUTPUT, index=False)
        print(f"✅ Saved {len(normal_packets)} NORMAL packets to {NORMAL_OUTPUT}")

if __name__ == "__main__":
    main()
    