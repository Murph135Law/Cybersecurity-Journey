#!/usr/bin/env python3
"""
Live Network Monitor (Scapy Version)
Real-time network traffic analysis using Scapy

Requirements: pip install scapy
Run with: sudo python3 network_monitor_scapy.py
"""

try:
    from scapy.all import *
except ImportError:
    print("Error: Scapy not installed")
    print("Install with: pip install scapy")
    sys.exit(1)

from collections import defaultdict
from datetime import datetime
import threading
import time

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class NetworkMonitor:
    """Real-time network traffic monitor using Scapy"""
    
    def __init__(self, interface=None, filter_str=None, display_mode='compact'):
        self.interface = interface
        self.filter_str = filter_str
        self.display_mode = display_mode
        
        # Statistics
        self.packet_count = 0
        self.protocol_stats = defaultdict(int)
        self.ip_stats = defaultdict(int)
        self.port_stats = defaultdict(int)
        self.connection_stats = defaultdict(int)
        self.start_time = datetime.now()
        self.lock = threading.Lock()
        
        # Common ports
        self.services = {
            20: 'FTP-DATA', 21: 'FTP', 22: 'SSH', 23: 'Telnet',
            25: 'SMTP', 53: 'DNS', 80: 'HTTP', 110: 'POP3',
            143: 'IMAP', 443: 'HTTPS', 445: 'SMB', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 6379: 'Redis',
            8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt', 27017: 'MongoDB'
        }
    
    def get_service_name(self, port):
        """Get service name for port"""
        return self.services.get(port, f'Port-{port}')
    
    def process_packet(self, packet):
        """Process captured packet"""
        with self.lock:
            self.packet_count += 1
        
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        # Get protocol info
        protocol = self.get_protocol(packet)
        
        # Update stats
        with self.lock:
            self.protocol_stats[protocol] += 1
        
        # Extract source and destination
        src_ip = None
        dst_ip = None
        src_port = None
        dst_port = None
        
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            with self.lock:
                self.ip_stats[src_ip] += 1
                self.ip_stats[dst_ip] += 1
        
        if TCP in packet:
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            
            with self.lock:
                self.port_stats[src_port] += 1
                self.port_stats[dst_port] += 1
                connection_key = f"{src_ip}:{src_port} -> {dst_ip}:{dst_port}"
                self.connection_stats[connection_key] += 1
        
        elif UDP in packet:
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            
            with self.lock:
                self.port_stats[src_port] += 1
                self.port_stats[dst_port] += 1
        
        # Display packet based on mode
        if self.display_mode == 'compact':
            self.display_compact(timestamp, packet, protocol, src_ip, dst_ip, src_port, dst_port)
        elif self.display_mode == 'detailed':
            self.display_detailed(timestamp, packet, protocol, src_ip, dst_ip, src_port, dst_port)
        elif self.display_mode == 'minimal':
            self.display_minimal(timestamp, protocol, src_ip, dst_ip)
    
    def get_protocol(self, packet):
        """Determine packet protocol"""
        if TCP in packet:
            return 'TCP'
        elif UDP in packet:
            return 'UDP'
        elif ICMP in packet:
            return 'ICMP'
        elif ARP in packet:
            return 'ARP'
        elif DNS in packet:
            return 'DNS'
        elif IP in packet:
            return 'IP'
        else:
            return 'OTHER'
    
    def display_compact(self, timestamp, packet, protocol, src_ip, dst_ip, src_port, dst_port):
        """Compact display format"""
        # Color based on protocol
        if protocol == 'TCP':
            proto_color = Colors.GREEN
        elif protocol == 'UDP':
            proto_color = Colors.BLUE
        elif protocol == 'ICMP':
            proto_color = Colors.YELLOW
        elif protocol == 'ARP':
            proto_color = Colors.CYAN
        elif protocol == 'DNS':
            proto_color = Colors.MAGENTA
        else:
            proto_color = Colors.ENDC
        
        output = f"{Colors.CYAN}[{timestamp}]{Colors.ENDC} "
        output += f"{proto_color}{protocol:8s}{Colors.ENDC} "
        
        if src_ip and dst_ip:
            output += f"{src_ip:15s} → {dst_ip:15s}"
            
            if src_port and dst_port:
                src_service = self.get_service_name(src_port)
                dst_service = self.get_service_name(dst_port)
                
                output += f" | {Colors.YELLOW}{src_port:5d}{Colors.ENDC}"
                if src_service and not src_service.startswith('Port-'):
                    output += f"({src_service})"
                output += f" → {Colors.YELLOW}{dst_port:5d}{Colors.ENDC}"
                if dst_service and not dst_service.startswith('Port-'):
                    output += f"({dst_service})"
                
                # TCP flags
                if TCP in packet:
                    flags = packet[TCP].flags
                    flag_str = str(flags)
                    if flag_str:
                        output += f" [{Colors.RED}{flag_str}{Colors.ENDC}]"
                
                # Packet size
                output += f" | {len(packet)} bytes"
        
        elif ARP in packet:
            output += f"{packet[ARP].psrc} → {packet[ARP].pdst}"
            if packet[ARP].op == 1:
                output += " (Who has?)"
            elif packet[ARP].op == 2:
                output += " (Is at)"
        
        print(output)
    
    def display_detailed(self, timestamp, packet, protocol, src_ip, dst_ip, src_port, dst_port):
        """Detailed display format"""
        print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
        print(f"{Colors.CYAN}[{timestamp}]{Colors.ENDC} Packet #{self.packet_count}")
        print(f"{Colors.YELLOW}Protocol:{Colors.ENDC} {protocol}")
        
        if src_ip and dst_ip:
            print(f"{Colors.YELLOW}Source:{Colors.ENDC} {src_ip}", end='')
            if src_port:
                print(f":{src_port} ({self.get_service_name(src_port)})", end='')
            print()
            
            print(f"{Colors.YELLOW}Destination:{Colors.ENDC} {dst_ip}", end='')
            if dst_port:
                print(f":{dst_port} ({self.get_service_name(dst_port)})", end='')
            print()
        
        if TCP in packet:
            print(f"{Colors.YELLOW}TCP Flags:{Colors.ENDC} {packet[TCP].flags}")
            print(f"{Colors.YELLOW}Seq:{Colors.ENDC} {packet[TCP].seq}, {Colors.YELLOW}Ack:{Colors.ENDC} {packet[TCP].ack}")
        
        if UDP in packet:
            print(f"{Colors.YELLOW}UDP Length:{Colors.ENDC} {packet[UDP].len}")
        
        if Raw in packet:
            payload = bytes(packet[Raw].load)
            if len(payload) > 0:
                print(f"{Colors.YELLOW}Payload ({len(payload)} bytes):{Colors.ENDC}")
                # Show first 64 bytes
                hex_dump = ' '.join(f'{b:02x}' for b in payload[:64])
                print(f"  {hex_dump}")
        
        print(f"{Colors.YELLOW}Packet Size:{Colors.ENDC} {len(packet)} bytes")
    
    def display_minimal(self, timestamp, protocol, src_ip, dst_ip):
        """Minimal display format"""
        if src_ip and dst_ip:
            print(f"[{timestamp}] {protocol:5s} {src_ip} → {dst_ip}")
    
    def display_stats_live(self):
        """Display live statistics in a separate thread"""
        while True:
            time.sleep(5)
            self.print_current_stats()
    
    def print_current_stats(self):
        """Print current statistics"""
        with self.lock:
            runtime = (datetime.now() - self.start_time).total_seconds()
            pps = self.packet_count / runtime if runtime > 0 else 0
            
            print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
            print(f"{Colors.GREEN}LIVE STATS{Colors.ENDC} | "
                  f"Packets: {self.packet_count} | "
                  f"PPS: {pps:.2f} | "
                  f"Runtime: {runtime:.0f}s")
            
            # Top protocols
            top_protos = sorted(self.protocol_stats.items(), key=lambda x: x[1], reverse=True)[:3]
            if top_protos:
                proto_str = ', '.join([f"{p}: {c}" for p, c in top_protos])
                print(f"{Colors.YELLOW}Top Protocols:{Colors.ENDC} {proto_str}")
            
            # Top IPs
            top_ips = sorted(self.ip_stats.items(), key=lambda x: x[1], reverse=True)[:3]
            if top_ips:
                ip_str = ', '.join([f"{ip}: {c}" for ip, c in top_ips])
                print(f"{Colors.YELLOW}Top IPs:{Colors.ENDC} {ip_str}")
            
            print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
    
    def print_final_stats(self):
        """Print final statistics"""
        with self.lock:
            runtime = (datetime.now() - self.start_time).total_seconds()
            
            print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
            print(f"{Colors.BOLD}{Colors.GREEN}FINAL STATISTICS{Colors.ENDC}")
            print(f"{Colors.BOLD}{'='*70}{Colors.ENDC}\n")
            
            print(f"{Colors.CYAN}Capture Duration:{Colors.ENDC} {runtime:.2f} seconds")
            print(f"{Colors.CYAN}Total Packets:{Colors.ENDC} {self.packet_count}")
            print(f"{Colors.CYAN}Average PPS:{Colors.ENDC} {self.packet_count/runtime:.2f}\n")
            
            # Protocol breakdown
            print(f"{Colors.YELLOW}Protocol Distribution:{Colors.ENDC}")
            for proto, count in sorted(self.protocol_stats.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / self.packet_count * 100) if self.packet_count > 0 else 0
                print(f"  {proto:10s}: {count:6d} ({percentage:5.2f}%)")
            
            # Top IPs
            print(f"\n{Colors.YELLOW}Top 10 IP Addresses:{Colors.ENDC}")
            for ip, count in sorted(self.ip_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {ip:15s}: {count:6d} packets")
            
            # Top Ports
            print(f"\n{Colors.YELLOW}Top 10 Ports:{Colors.ENDC}")
            for port, count in sorted(self.port_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
                service = self.get_service_name(port)
                print(f"  {port:5d} ({service:15s}): {count:6d} packets")
            
            # Top Connections
            if self.connection_stats:
                print(f"\n{Colors.YELLOW}Top 10 Connections:{Colors.ENDC}")
                for conn, count in sorted(self.connection_stats.items(), key=lambda x: x[1], reverse=True)[:10]:
                    print(f"  {conn}: {count} packets")
            
            print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    
    def start(self):
        """Start packet capture"""
        print(f"\n{Colors.GREEN}{Colors.BOLD}Starting packet capture...{Colors.ENDC}")
        
        if self.interface:
            print(f"{Colors.YELLOW}Interface:{Colors.ENDC} {self.interface}")
        
        if self.filter_str:
            print(f"{Colors.YELLOW}Filter:{Colors.ENDC} {self.filter_str}")
        
        print(f"{Colors.YELLOW}Display Mode:{Colors.ENDC} {self.display_mode}")
        print(f"{Colors.YELLOW}Press Ctrl+C to stop{Colors.ENDC}\n")
        
        # Start live stats display thread
        stats_thread = threading.Thread(target=self.display_stats_live, daemon=True)
        stats_thread.start()
        
        try:
            # Start sniffing
            sniff(iface=self.interface, 
                  filter=self.filter_str, 
                  prn=self.process_packet, 
                  store=False)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Stopping capture...{Colors.ENDC}")
        finally:
            self.print_final_stats()

def print_banner():
    """Print application banner"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("=" * 70)
    print("           LIVE NETWORK MONITOR (Scapy)")
    print("=" * 70)
    print(f"{Colors.ENDC}")

def list_interfaces():
    """List available network interfaces"""
    print(f"\n{Colors.YELLOW}Available Interfaces:{Colors.ENDC}")
    try:
        ifaces = get_if_list()
        for i, iface in enumerate(ifaces, 1):
            print(f"  {i}. {iface}")
        return ifaces
    except:
        print(f"  {Colors.RED}Could not list interfaces{Colors.ENDC}")
        return []

def is_admin():
    """Check if running with admin/root privileges"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        # Unix/Linux/Mac
        import os
        return os.geteuid() == 0

def main():
    print_banner()
    
    # Check for root/admin
    if not is_admin():
        print(f"{Colors.RED}Error: This script requires administrator privileges{Colors.ENDC}")
        if sys.platform == 'win32':
            print(f"{Colors.YELLOW}Windows: Right-click Python and 'Run as Administrator'{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}Linux/Mac: Run with sudo: sudo python3 {sys.argv[0]}{Colors.ENDC}")
        sys.exit(1)
    
    # Configuration menu
    print(f"\n{Colors.YELLOW}Configuration:{Colors.ENDC}")
    
    # Interface selection
    ifaces = list_interfaces()
    iface_choice = input(f"\n{Colors.GREEN}Select interface (number or name, blank for all): {Colors.ENDC}").strip()
    
    interface = None
    if iface_choice:
        try:
            idx = int(iface_choice) - 1
            if 0 <= idx < len(ifaces):
                interface = ifaces[idx]
        except ValueError:
            interface = iface_choice
    
    # Filter selection
    print(f"\n{Colors.YELLOW}Filter Options:{Colors.ENDC}")
    print("  1. All traffic")
    print("  2. TCP only")
    print("  3. UDP only")
    print("  4. ICMP only")
    print("  5. HTTP/HTTPS (ports 80, 443)")
    print("  6. DNS (port 53)")
    print("  7. Custom BPF filter")
    
    filter_choice = input(f"\n{Colors.GREEN}Select filter: {Colors.ENDC}").strip()
    
    filter_str = None
    if filter_choice == '2':
        filter_str = 'tcp'
    elif filter_choice == '3':
        filter_str = 'udp'
    elif filter_choice == '4':
        filter_str = 'icmp'
    elif filter_choice == '5':
        filter_str = 'tcp port 80 or tcp port 443'
    elif filter_choice == '6':
        filter_str = 'udp port 53'
    elif filter_choice == '7':
        filter_str = input(f"{Colors.GREEN}Enter BPF filter: {Colors.ENDC}").strip()
    
    # Display mode
    print(f"\n{Colors.YELLOW}Display Mode:{Colors.ENDC}")
    print("  1. Compact (default)")
    print("  2. Detailed")
    print("  3. Minimal")
    
    mode_choice = input(f"\n{Colors.GREEN}Select mode: {Colors.ENDC}").strip()
    
    display_mode = 'compact'
    if mode_choice == '2':
        display_mode = 'detailed'
    elif mode_choice == '3':
        display_mode = 'minimal'
    
    # Create and start monitor
    monitor = NetworkMonitor(interface=interface, filter_str=filter_str, display_mode=display_mode)
    monitor.start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)