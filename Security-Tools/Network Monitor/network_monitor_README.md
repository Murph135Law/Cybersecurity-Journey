# Live Network Traffic Monitor

Real-time network packet capture and analysis tool using Scapy. Built for security monitoring, traffic analysis, and network troubleshooting.

## Overview

This tool provides real-time visibility into network traffic with protocol identification, connection tracking, and live statistics. Designed for security analysts, network administrators, and anyone learning network security fundamentals.

## Features

- **Real-Time Packet Capture**: Live monitoring of network traffic as it happens
- **Protocol Identification**: Automatic detection of TCP, UDP, ICMP, ARP, DNS, and more
- **Service Detection**: Identifies common services by port (HTTP, SSH, MySQL, RDP, etc.)
- **Multiple Display Modes**: 
  - Compact: Balanced view with key packet details
  - Detailed: Full packet information including payloads
  - Minimal: Basic traffic flow only
- **Live Statistics**: 
  - Packets per second (PPS)
  - Protocol distribution
  - Top IPs and ports
  - Active connections
- **Flexible Filtering**: BPF filters to focus on specific traffic types
- **Connection Tracking**: Monitor communication patterns between hosts
- **Colored Output**: Easy-to-read terminal output with protocol-based color coding

## Requirements

**Python Version**: Python 3.6+

**Required Package**:
```bash
pip install scapy
```

**System Requirements**:
- **Administrator/Root privileges required** for packet capture
- Works on Linux, macOS, and Windows
- Network interface in promiscuous mode (handled automatically by Scapy)

## Installation

### Linux/macOS:

```bash
# Install Scapy
pip install scapy

# Or with pip3
pip3 install scapy

# Make script executable
chmod +x network_monitor.py
```

### Windows:

1. Install Npcap from https://npcap.com/
2. Install Scapy:
```bash
pip install scapy
```

## Usage

### Linux/macOS:
```bash
sudo python3 network_monitor.py
```

### Windows:
Run Command Prompt or PowerShell as Administrator:
```bash
python network_monitor.py
```

### Interactive Configuration

The tool will guide you through configuration:

1. **Select Network Interface**
   - View available interfaces
   - Choose specific interface or monitor all
   
2. **Choose Traffic Filter**
   - All traffic (no filter)
   - TCP only
   - UDP only
   - ICMP only
   - HTTP/HTTPS (ports 80, 443)
   - DNS (port 53)
   - Custom BPF filter

3. **Select Display Mode**
   - Compact (recommended for most use cases)
   - Detailed (full packet information)
   - Minimal (basic flow only)

### Example Session

```
==============================================================
           LIVE NETWORK MONITOR (Scapy)
==============================================================

Available Interfaces:
  1. eth0
  2. wlan0
  3. lo

Select interface (number or name, blank for all): 2

Filter Options:
  1. All traffic
  2. TCP only
  3. UDP only
  4. ICMP only
  5. HTTP/HTTPS (ports 80, 443)
  6. DNS (port 53)
  7. Custom BPF filter

Select filter: 5

Display Mode:
  1. Compact (default)
  2. Detailed
  3. Minimal

Select mode: 1

Starting packet capture...
Interface: wlan0
Filter: tcp port 80 or tcp port 443
Display Mode: compact
Press Ctrl+C to stop

[14:32:15.421] TCP      192.168.1.100   → 172.217.14.206  |  5432 → 443(HTTPS) [PA] | 1420 bytes
[14:32:15.456] TCP      172.217.14.206  → 192.168.1.100   |   443(HTTPS) → 5432 [PA] | 1380 bytes
[14:32:15.502] TCP      192.168.1.100   → 93.184.216.34   |  5433 → 80(HTTP) [S] | 60 bytes

============================================================
LIVE STATS | Packets: 1247 | PPS: 24.53 | Runtime: 51s
Top Protocols: TCP: 1156, UDP: 89, ICMP: 2
Top IPs: 192.168.1.100: 634, 172.217.14.206: 289, 93.184.216.34: 178
============================================================
```

## Display Modes Explained

### Compact Mode (Recommended)
Shows essential packet information in a single line:
- Timestamp
- Protocol (color-coded)
- Source IP and port
- Destination IP and port
- Service names
- TCP flags (if applicable)
- Packet size

Perfect for monitoring traffic patterns without overwhelming detail.

### Detailed Mode
Shows comprehensive packet information:
- All fields from compact mode
- TCP sequence/acknowledgment numbers
- Payload preview (first 64 bytes in hex)
- Layer-specific details
- Full packet structure

Use when investigating specific connections or debugging.

### Minimal Mode
Shows only basic flow information:
- Timestamp
- Protocol
- Source IP → Destination IP

Useful for high-volume traffic or when you only need connection patterns.

## Common Use Cases

### 1. Monitor Web Traffic
```
Filter: HTTP/HTTPS (ports 80, 443)
Mode: Compact
Use: See all web requests from your network
```

### 2. Detect Port Scans
```
Filter: All traffic
Mode: Compact
Watch for: Multiple SYN packets to sequential ports from single IP
```

### 3. Troubleshoot DNS Issues
```
Filter: DNS (port 53)
Mode: Detailed
Use: See DNS queries and responses
```

### 4. Analyze Application Traffic
```
Filter: Custom (tcp port 3306) for MySQL
Mode: Detailed
Use: Monitor database connections
```

### 5. Network Baseline
```
Filter: All traffic
Mode: Compact
Use: Understand normal traffic patterns
Duration: Run for 5-10 minutes, review statistics
```

## Recognized Services

The monitor automatically identifies these common services:

| Port  | Service       | Port  | Service        |
|-------|---------------|-------|----------------|
| 20    | FTP-DATA      | 3306  | MySQL          |
| 21    | FTP           | 3389  | RDP            |
| 22    | SSH           | 5432  | PostgreSQL     |
| 23    | Telnet        | 6379  | Redis          |
| 25    | SMTP          | 8080  | HTTP-Proxy     |
| 53    | DNS           | 8443  | HTTPS-Alt      |
| 80    | HTTP          | 27017 | MongoDB        |
| 110   | POP3          |       |                |
| 143   | IMAP          |       |                |
| 443   | HTTPS         |       |                |
| 445   | SMB           |       |                |

## Statistics Explained

### Live Statistics (Updated Every 5 Seconds)
- **Total Packets**: Cumulative count since start
- **PPS (Packets Per Second)**: Current capture rate
- **Runtime**: Time since capture started
- **Top Protocols**: Most common protocols and their packet counts
- **Top IPs**: Most active IP addresses

### Final Statistics (Shown on Exit)
- **Capture Duration**: Total monitoring time
- **Protocol Distribution**: Breakdown by protocol with percentages
- **Top IP Addresses**: Most active hosts
- **Top Ports**: Most used ports with service names
- **Top Connections**: Most active source → destination pairs

## BPF Filter Examples

Berkeley Packet Filter syntax for custom filtering:

```bash
# Specific host
host 192.168.1.1

# Specific port
port 22

# Port range
portrange 8000-9000

# Multiple conditions (AND)
tcp and port 80 and host 192.168.1.1

# Multiple conditions (OR)
tcp port 80 or tcp port 443

# Exclude traffic
not port 22

# Subnet
net 192.168.1.0/24

# Incoming traffic only
dst host 192.168.1.100

# Outgoing traffic only
src host 192.168.1.100
```

## Performance Considerations

- **High Traffic Networks**: Use filters to reduce packet volume
- **CPU Usage**: Detailed mode is more CPU-intensive than compact mode
- **Storage**: Tool doesn't save packets (real-time only, no disk writes)
- **Promiscuous Mode**: May capture traffic not destined for your interface

## Troubleshooting

### "This script requires administrator privileges"
**Solution**: Run with `sudo` (Linux/Mac) or as Administrator (Windows)

### "Scapy not installed"
**Solution**: `pip install scapy` or `pip3 install scapy`

### Windows: "Npcap not found"
**Solution**: Install Npcap from https://npcap.com/

### No packets captured
**Possible causes**:
- Wrong interface selected (try different interface or all interfaces)
- Filter too restrictive (try "All traffic" first)
- Network inactive (generate traffic by browsing web)
- Firewall blocking promiscuous mode

### "Could not list interfaces"
**Solution**: 
- Check Scapy installation: `python3 -c "from scapy.all import *; print(get_if_list())"`
- Ensure running with admin/root privileges

## Security and Legal Considerations

**Important**: This tool captures network traffic, which may include sensitive data.

### Legal Use Only
- **Personal Networks**: Monitor your own devices and networks
- **Authorized Testing**: Only use on networks you own or have written permission to monitor
- **Corporate Networks**: Obtain IT department approval before use
- **Educational Use**: Acceptable in lab/test environments

### Never Use For
- Monitoring networks without authorization
- Intercepting others' communications
- Corporate espionage or competitive intelligence
- Any illegal surveillance activity

Unauthorized network monitoring may violate:
- Wiretap laws
- Computer Fraud and Abuse Act (CFAA) - United States
- Computer Misuse Act - United Kingdom
- Similar laws in other jurisdictions

**Always obtain proper authorization before monitoring any network traffic.**

## Privacy Considerations

This tool can capture:
- IP addresses and communication patterns
- Unencrypted data (HTTP, FTP, Telnet, etc.)
- DNS queries (reveals websites visited)
- Connection metadata

**Best Practices**:
- Only monitor traffic you're authorized to see
- Don't save or share captured data without consent
- Use filters to limit capture to necessary traffic
- Be aware of data protection regulations (GDPR, CCPA, etc.)

## Technical Details

### Packet Processing Flow
1. Scapy captures raw packets from network interface
2. Packet layers extracted (Ethernet → IP → TCP/UDP/ICMP)
3. Protocol and service identification
4. Statistics updated (thread-safe with locks)
5. Display formatted based on selected mode
6. Live stats thread updates every 5 seconds

### Threading Model
- Main thread: Packet capture (Scapy sniff function)
- Background thread: Live statistics display (daemon thread)
- Thread synchronization: Lock-based for statistics updates

### Color Coding
- **Green**: TCP traffic
- **Blue**: UDP traffic  
- **Yellow**: ICMP traffic / Port numbers
- **Cyan**: ARP traffic / Timestamps
- **Magenta**: DNS traffic
- **Red**: TCP flags

## Limitations

- Real-time only (no packet storage or PCAP export)
- Cannot decrypt encrypted traffic (HTTPS, SSH, etc.)
- May miss packets on very high-traffic networks
- Limited to single interface at a time (unless monitoring all)
- No packet manipulation (capture only, not injection)

## Future Enhancements

Potential improvements for future versions:
- [ ] PCAP file export
- [ ] Packet filtering by saved rules
- [ ] Geolocation of IP addresses
- [ ] Automatic threat detection patterns
- [ ] Web-based dashboard
- [ ] Multiple interface monitoring simultaneously
- [ ] Historical traffic analysis
- [ ] Alert system for suspicious patterns

## Learning Value

This project demonstrates:
- Network fundamentals (TCP/IP, protocols, ports)
- Python networking with Scapy
- Multithreading and thread safety
- Real-time data processing
- Statistics collection and analysis
- User interface design for terminal applications
- Security tool development

## Author

**Marcus-J Gomes-Luis**  
Career Changer: Hospitality Management → Cybersecurity

**Certifications**: CompTIA CySA+, Security+, Network+  
**Training**: Top 2% on TryHackMe | Harvard CS50P (Week 6/10)  
**GitHub**: [https://github.com/Murph135Law]  
**LinkedIn**: [linkedin.com/in/marcus-j-gomes-luis-33297a233](https://linkedin.com/in/marcus-j-gomes-luis-33297a233)

**Status**: Seeking SOC Analyst / Security Analyst roles (Remote or Cape Town, SA)  
**Available**: May 2026

## From Hospitality to Security Operations

This network monitor reflects skills directly transferable from managing restaurant operations:

**Restaurant Crisis at 2am:**
- Multiple systems failing
- Need immediate visibility into what's happening
- Identify root cause quickly
- Track multiple issues simultaneously
- Make decisions under pressure

**Network Security Monitoring:**
- Multiple alerts firing
- Need immediate visibility into traffic patterns
- Identify malicious activity quickly
- Track multiple connections simultaneously  
- Make decisions under pressure

The mindset is the same. The tools are different.

## Contributing

This is an educational project built during my career transition. Feedback, suggestions, and constructive criticism welcome! 

## Acknowledgments

Built with [Scapy](https://scapy.net/) - the powerful Python packet manipulation library.

## License

Educational use. Use responsibly and only on authorized networks.

---

**Monitor responsibly. Learn continuously. Build deliberately.**
