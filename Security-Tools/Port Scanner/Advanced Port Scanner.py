#!/usr/bin/env python3
"""
Enhanced Port Scanner
Features: Multithreading, service detection, banner grabbing, colored output
"""

import socket
import threading
from queue import Queue
from datetime import datetime
import sys

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Common port-to-service mapping
COMMON_PORTS = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    53: 'DNS',
    80: 'HTTP',
    110: 'POP3',
    143: 'IMAP',
    443: 'HTTPS',
    445: 'SMB',
    3306: 'MySQL',
    3389: 'RDP',
    5432: 'PostgreSQL',
    5900: 'VNC',
    8080: 'HTTP-Proxy',
    8443: 'HTTPS-Alt'
}

def banner_grab(ip, port, timeout=2):
    """
    Attempt to grab service banner for identification
    Returns the banner string or None
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        
        # Send a generic request (works for many services)
        try:
            sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
        except:
            pass
        
        # Try to receive banner
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner[:100] if banner else None  # Limit banner length
    except:
        return None

def scan_port(ip, port, timeout=1):
    """
    Scan a single port on target IP
    Returns: (port, is_open, service_name, banner)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            service = COMMON_PORTS.get(port, 'Unknown')
            banner = banner_grab(ip, port)
            return (port, True, service, banner)
        else:
            return (port, False, None, None)
    except socket.error:
        return (port, False, None, None)

def worker(ip, port_queue, results, timeout):
    """
    Worker thread function to scan ports from queue
    """
    while not port_queue.empty():
        port = port_queue.get()
        result = scan_port(ip, port, timeout)
        results.append(result)
        port_queue.task_done()

def threaded_scan(ip, ports, num_threads=100, timeout=1):
    """
    Perform multithreaded port scan
    """
    port_queue = Queue()
    results = []
    
    # Fill queue with ports
    for port in ports:
        port_queue.put(port)
    
    # Create and start threads
    threads = []
    for _ in range(min(num_threads, len(ports))):
        thread = threading.Thread(target=worker, args=(ip, port_queue, results, timeout))
        thread.daemon = True
        thread.start()
        threads.append(thread)
    
    # Wait for all threads to complete
    port_queue.join()
    
    return results

def validate_ip(ip):
    """
    Validate IP address format
    """
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def resolve_hostname(hostname):
    """
    Resolve hostname to IP address
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def print_banner():
    """
    Print scanner banner
    """
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print("=" * 60)
    print("          PYTHON PORT SCANNER v2.0")
    print("=" * 60)
    print(f"{Colors.ENDC}")

def main():
    print_banner()
    
    # Get target from user
    target = input(f"{Colors.YELLOW}Enter IP or hostname to scan: {Colors.ENDC}").strip()
    
    # Validate/resolve target
    if validate_ip(target):
        ip = target
    else:
        print(f"{Colors.YELLOW}Resolving hostname...{Colors.ENDC}")
        ip = resolve_hostname(target)
        if not ip:
            print(f"{Colors.RED}Error: Could not resolve hostname{Colors.ENDC}")
            sys.exit(1)
        print(f"{Colors.GREEN}Resolved to: {ip}{Colors.ENDC}")
    
    # Choose scan type
    print(f"\n{Colors.YELLOW}Scan Options:{Colors.ENDC}")
    print("1. Quick Scan (Top 20 ports)")
    print("2. Common Scan (Top 100 ports)")
    print("3. Full Scan (All 65535 ports)")
    print("4. Custom port range")
    
    choice = input(f"{Colors.YELLOW}Choose scan type (1-4): {Colors.ENDC}").strip()
    
    # Define port list based on choice
    if choice == '1':
        ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 
                 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]
        num_threads = 20
    elif choice == '2':
        # Top 100 most common ports
        ports = list(range(1, 101)) + [110, 135, 139, 143, 443, 445, 993, 995, 
                                        1723, 3306, 3389, 5432, 5900, 8080, 8443]
        num_threads = 50
    elif choice == '3':
        ports = range(1, 65536)
        num_threads = 200
        print(f"{Colors.RED}Warning: Full scan will take a while!{Colors.ENDC}")
    elif choice == '4':
        try:
            start = int(input("Start port: "))
            end = int(input("End port: "))
            if 1 <= start <= end <= 65535:
                ports = range(start, end + 1)
                num_threads = 100
            else:
                print(f"{Colors.RED}Invalid port range{Colors.ENDC}")
                sys.exit(1)
        except ValueError:
            print(f"{Colors.RED}Invalid input{Colors.ENDC}")
            sys.exit(1)
    else:
        print(f"{Colors.RED}Invalid choice{Colors.ENDC}")
        sys.exit(1)
    
    # Start scan
    print(f"\n{Colors.BLUE}Starting scan on {ip}...{Colors.ENDC}")
    print(f"{Colors.BLUE}Scanning {len(list(ports))} ports with {num_threads} threads{Colors.ENDC}")
    print(f"{Colors.BLUE}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}\n")
    
    start_time = datetime.now()
    
    # Perform scan
    results = threaded_scan(ip, ports, num_threads)
    
    # Sort results by port number
    results.sort(key=lambda x: x[0])
    
    # Display results
    open_ports = [r for r in results if r[1]]
    
    print(f"\n{Colors.BOLD}SCAN RESULTS:{Colors.ENDC}")
    print("=" * 60)
    
    if open_ports:
        print(f"{Colors.GREEN}Found {len(open_ports)} open port(s):{Colors.ENDC}\n")
        
        for port, is_open, service, banner in open_ports:
            print(f"{Colors.GREEN}[+] Port {port:5d} | {service:15s} | OPEN{Colors.ENDC}")
            if banner:
                print(f"    {Colors.YELLOW}Banner: {banner}{Colors.ENDC}")
    else:
        print(f"{Colors.RED}No open ports found{Colors.ENDC}")
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print(f"{Colors.BLUE}Scan completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    print(f"{Colors.BLUE}Duration: {duration:.2f} seconds{Colors.ENDC}")
    print(f"{Colors.BLUE}Ports scanned: {len(results)}{Colors.ENDC}")
    print(f"{Colors.BLUE}Open ports: {len(open_ports)}{Colors.ENDC}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Scan interrupted by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)