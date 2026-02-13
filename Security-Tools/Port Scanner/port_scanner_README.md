# Advanced Port Scanner

A fast, multithreaded Python port scanner with banner grabbing, service detection, and colored terminal output. Built as part of my transition from hospitality management to cybersecurity.

## Overview

This tool provides efficient network reconnaissance capabilities with multiple scan modes, automatic service identification, and real-time banner grabbing to identify running services on target systems.

## Features

- **Multithreaded Scanning**: Up to 200 concurrent threads for fast scanning
- **Banner Grabbing**: Attempts to retrieve service banners for accurate identification
- **Service Detection**: Automatically identifies common services (HTTP, SSH, FTP, MySQL, etc.)
- **Multiple Scan Modes**: 
  - Quick Scan (Top 20 ports)
  - Common Scan (Top 100 ports)
  - Full Scan (All 65,535 ports)
  - Custom Range (User-defined port range)
- **Hostname Resolution**: Automatically resolves hostnames to IP addresses
- **Colored Output**: Easy-to-read terminal output with color-coded results
- **Performance Metrics**: Displays scan duration and summary statistics

## Requirements

**Python Version**: Python 3.6+

**Standard Library Modules** (no installation needed):
- `socket`
- `threading`
- `queue`
- `datetime`
- `sys`

## Installation

1. Clone or download the script
2. Ensure Python 3 is installed
3. No additional dependencies required (uses Python standard library)

```bash
# Verify Python version
python3 --version

# Make script executable (Linux/Mac)
chmod +x port_scanner.py
```

## Usage

### Basic Usage

```bash
python3 port_scanner.py
```

### Interactive Prompts

The scanner will prompt you for:

1. **Target**: Enter IP address or hostname
   ```
   Enter IP or hostname to scan: 192.168.1.1
   ```

2. **Scan Type**: Choose your scan mode
   ```
   1. Quick Scan (Top 20 ports)
   2. Common Scan (Top 100 ports)
   3. Full Scan (All 65535 ports)
   4. Custom port range
   ```

3. **Results**: View open ports with service names and banners

### Example Session

```
==============================================================
          PYTHON PORT SCANNER v2.0
==============================================================

Enter IP or hostname to scan: scanme.nmap.org
Resolving hostname...
Resolved to: 45.33.32.156

Scan Options:
1. Quick Scan (Top 20 ports)
2. Common Scan (Top 100 ports)
3. Full Scan (All 65535 ports)
4. Custom port range
Choose scan type (1-4): 1

Starting scan on 45.33.32.156...
Scanning 20 ports with 20 threads
Started at: 2026-02-14 14:30:15

SCAN RESULTS:
==============================================================
Found 3 open port(s):

[+] Port    22 | SSH             | OPEN
    Banner: SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5
[+] Port    80 | HTTP            | OPEN
    Banner: HTTP/1.1 200 OK
[+] Port   443 | HTTPS           | OPEN

==============================================================
Scan completed at: 2026-02-14 14:30:18
Duration: 3.42 seconds
Ports scanned: 20
Open ports: 3
==============================================================
```

## Supported Services

The scanner recognizes these common services:

| Port  | Service      | Port  | Service        |
|-------|--------------|-------|----------------|
| 21    | FTP          | 3306  | MySQL          |
| 22    | SSH          | 3389  | RDP            |
| 23    | Telnet       | 5432  | PostgreSQL     |
| 25    | SMTP         | 5900  | VNC            |
| 53    | DNS          | 8080  | HTTP-Proxy     |
| 80    | HTTP         | 8443  | HTTPS-Alt      |
| 110   | POP3         |       |                |
| 143   | IMAP         |       |                |
| 443   | HTTPS        |       |                |
| 445   | SMB          |       |                |

## Scan Modes Explained

### 1. Quick Scan (Recommended for initial reconnaissance)
- Scans 20 most common ports
- Fast execution (typically < 10 seconds)
- Good for quick service discovery

### 2. Common Scan (Balanced approach)
- Scans top 100 commonly used ports
- Moderate speed (typically 15-30 seconds)
- Comprehensive coverage of standard services

### 3. Full Scan (Thorough but slow)
- Scans all 65,535 ports
- Can take 10+ minutes depending on network and timeout settings
- Use only when comprehensive coverage is required

### 4. Custom Range (Targeted scanning)
- Scan specific port ranges
- Example: Scan ports 8000-9000 for web services
- Useful when investigating specific service types

## Performance Considerations

- **Threading**: More threads = faster scans, but may trigger IDS/IPS systems
- **Timeout**: Default 1 second per port; adjust based on network conditions
- **Network Load**: Full scans generate significant network traffic
- **Target Stability**: Some devices may respond poorly to aggressive scanning

## Technical Details

### Banner Grabbing Method
The scanner attempts to connect to open ports and sends a generic HTTP request to elicit a banner response. This helps identify the specific service version running on the port.

### Threading Model
Uses Python's `threading` and `queue` modules to implement a worker pool pattern, allowing concurrent port scanning while managing system resources efficiently.

### Error Handling
- Graceful handling of connection timeouts
- Keyboard interrupt (Ctrl+C) support
- Invalid input validation
- Network error management

## Limitations

- Banner grabbing may not work for all services
- Some services may not respond to generic probes
- Firewalls and security devices may block or rate-limit scan attempts
- Scan accuracy depends on network conditions and target responsiveness

## Legal and Ethical Use

**Important**: This tool is designed for:
- Authorized security assessments
- Personal network auditing
- Educational purposes
- Penetration testing with explicit permission

**Never use this tool against systems you do not own or have explicit written authorization to test.**

Unauthorized port scanning may be illegal in your jurisdiction and can violate:
- Computer Fraud and Abuse Act (CFAA) in the United States
- Computer Misuse Act in the United Kingdom
- Similar laws in other countries

## Troubleshooting

### "Could not resolve hostname"
- Check spelling of hostname
- Verify DNS is working
- Try using IP address directly

### "No open ports found" (when ports should be open)
- Target may be firewalled
- Try increasing timeout value in code
- Check network connectivity to target

### Slow scan performance
- Reduce number of threads
- Use Quick Scan instead of Full Scan
- Check network latency to target

## Future Enhancements

Potential improvements for future versions:
- [ ] OS fingerprinting
- [ ] Save results to file (CSV, JSON, XML)
- [ ] Integration with vulnerability databases
- [ ] UDP port scanning support
- [ ] Stealth scanning techniques
- [ ] GUI interface

## Author

**Marcus-J Gomes-Luis**  
Career Changer: Hospitality Management → Cybersecurity

**Certifications**: CompTIA CySA+, Security+, Network+  
**Training**: Top 2% on TryHackMe | Harvard CS50P  
**GitHub**: [https://github.com/Murph135Law]  
**LinkedIn**: [linkedin.com/in/marcus-j-gomes-luis-33297a233](https://linkedin.com/in/marcus-j-gomes-luis-33297a233)

**Status**: Seeking SOC Analyst / Security Analyst roles (Remote or Cape Town, SA)  
**Available**: May 2026

## Learning Journey

This port scanner was built as part of my transition from 20 years in hospitality operations management to cybersecurity. It demonstrates practical application of:
- Python networking with sockets
- Multithreading for concurrent operations
- Service enumeration techniques
- Security tool development
- Code documentation and project structure

The experience gained from managing high-pressure restaurant operations translates directly to security operations: staying calm under pressure, rapid problem triage, and systematic troubleshooting.

## Contributing

This is an educational project, but feedback and suggestions are welcome! Feel free to:
- Report issues
- Suggest improvements
- Share your use cases

## License

This project is provided for educational purposes. Use responsibly and ethically.

---

**Built with determination. Tested with curiosity. Shared for learning.**
