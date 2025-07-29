"""
Advanced Network Security Scanner Module
"""

import socket
import threading
import time
import struct
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor
import ipaddress
from wolf.core.base import BaseModule

class NetworkScannerModule(BaseModule):
    """
    Advanced network scanning and reconnaissance capabilities
    """
    
    def __init__(self):
        super().__init__("NetworkScanner")
        self.open_ports = []
        self.live_hosts = []
        self.lock = threading.Lock()
    
    def execute(self, target, **kwargs):
        """
        Execute network scanning operations
        
        Args:
            target (str): Target IP/CIDR/hostname
            **kwargs: Additional parameters
            
        Returns:
            dict: Scan results
        """
        return self.comprehensive_scan(target=target, **kwargs)
    
    def comprehensive_scan(self, target, port_range=None, **kwargs):
        """
        Perform comprehensive network scan
        
        Args:
            target (str): Target to scan
            port_range (str): Port range (e.g., "1-1000")
            **kwargs: Additional parameters
            
        Returns:
            dict: Comprehensive scan results
        """
        self.log_info(f"Starting comprehensive network scan for {target}")
        
        results = {
            'target': target,
            'host_discovery': {},
            'port_scan': {},
            'service_detection': {},
            'os_detection': {},
            'vulnerability_scan': {},
            'network_topology': {},
            'timing': {}
        }
        
        start_time = time.time()
        
        try:
            # Host Discovery
            results['host_discovery'] = self._discover_hosts(target, **kwargs)
            
            # Port Scanning
            if port_range:
                results['port_scan'] = self._scan_ports(target, port_range, **kwargs)
            
            # Service Detection
            if results['port_scan'].get('open_ports'):
                results['service_detection'] = self._detect_services(
                    target, results['port_scan']['open_ports'], **kwargs
                )
            
            # OS Detection
            results['os_detection'] = self._detect_os(target, **kwargs)
            
            # Network Topology
            results['network_topology'] = self._analyze_topology(target, **kwargs)
            
            # Vulnerability Scanning
            results['vulnerability_scan'] = self._scan_vulnerabilities(target, **kwargs)
            
            results['timing']['total_duration'] = time.time() - start_time
            
            self.log_info(f"Network scan complete in {results['timing']['total_duration']:.2f} seconds")
            
        except Exception as e:
            self.log_error(f"Network scanning error: {e}")
            results['error'] = str(e)
        
        return results
    
    def _discover_hosts(self, target, **kwargs):
        """Discover live hosts in network"""
        discovery_results = {
            'method': 'ping_sweep',
            'live_hosts': [],
            'scan_range': target,
            'total_hosts_scanned': 0
        }
        
        try:
            # Handle different target formats
            if '/' in target:  # CIDR notation
                network = ipaddress.ip_network(target, strict=False)
                hosts_to_scan = list(network.hosts())
            elif '-' in target:  # IP range
                start_ip, end_ip = target.split('-')
                start = ipaddress.ip_address(start_ip.strip())
                end = ipaddress.ip_address(end_ip.strip())
                hosts_to_scan = [ipaddress.ip_address(ip) for ip in range(int(start), int(end) + 1)]
            else:  # Single host
                hosts_to_scan = [ipaddress.ip_address(target)]
            
            discovery_results['total_hosts_scanned'] = len(hosts_to_scan)
            
            # Ping sweep with threading
            max_threads = kwargs.get('threads', 50)
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = [executor.submit(self._ping_host, str(host)) for host in hosts_to_scan]
                
                for future in futures:
                    result = future.result()
                    if result['alive']:
                        discovery_results['live_hosts'].append(result)
            
        except Exception as e:
            self.log_error(f"Host discovery error: {e}")
        
        return discovery_results
    
    def _ping_host(self, host):
        """Ping individual host"""
        result = {
            'ip': host,
            'alive': False,
            'response_time': None,
            'method': 'ping'
        }
        
        try:
            # Use system ping command
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", "1000", host]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", host]
            
            start_time = time.time()
            proc = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            
            if proc.returncode == 0:
                result['alive'] = True
                result['response_time'] = (time.time() - start_time) * 1000
                
                with self.lock:
                    self.live_hosts.append(host)
                    self.log_info(f"Host alive: {host}")
        
        except Exception as e:
            self.log_debug(f"Ping error for {host}: {e}")
        
        return result
    
    def _scan_ports(self, target, port_range, **kwargs):
        """Scan ports on target"""
        port_results = {
            'target': target,
            'port_range': port_range,
            'open_ports': [],
            'closed_ports': [],
            'filtered_ports': [],
            'scan_method': 'tcp_connect'
        }
        
        try:
            # Parse port range
            if '-' in port_range:
                start_port, end_port = map(int, port_range.split('-'))
                ports_to_scan = range(start_port, end_port + 1)
            else:
                ports_to_scan = [int(port_range)]
            
            # Port scanning with threading
            timeout = kwargs.get('timeout', 1)
            max_threads = kwargs.get('threads', 100)
            
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = [
                    executor.submit(self._scan_port, target, port, timeout) 
                    for port in ports_to_scan
                ]
                
                for future in futures:
                    result = future.result()
                    if result['state'] == 'open':
                        port_results['open_ports'].append(result)
                    elif result['state'] == 'closed':
                        port_results['closed_ports'].append(result)
                    else:
                        port_results['filtered_ports'].append(result)
            
        except Exception as e:
            self.log_error(f"Port scanning error: {e}")
        
        return port_results
    
    def _scan_port(self, host, port, timeout):
        """Scan individual port"""
        result = {
            'port': port,
            'state': 'filtered',
            'service': None,
            'banner': None
        }
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            connect_result = sock.connect_ex((host, port))
            
            if connect_result == 0:
                result['state'] = 'open'
                
                # Try to grab banner
                try:
                    sock.send(b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\n\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore')
                    if banner:
                        result['banner'] = banner[:200]  # Limit banner size
                except:
                    pass
                
                with self.lock:
                    self.open_ports.append({'host': host, 'port': port})
                    self.log_info(f"Open port: {host}:{port}")
            else:
                result['state'] = 'closed'
            
            sock.close()
            
        except socket.timeout:
            result['state'] = 'filtered'
        except Exception as e:
            self.log_debug(f"Port scan error {host}:{port}: {e}")
        
        return result
    
    def _detect_services(self, target, open_ports, **kwargs):
        """Detect services running on open ports"""
        service_results = {
            'services_detected': [],
            'method': 'banner_grabbing'
        }
        
        # Common service mappings
        common_services = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            3389: 'RDP',
            3306: 'MySQL',
            5432: 'PostgreSQL',
            6379: 'Redis',
            27017: 'MongoDB'
        }
        
        try:
            for port_info in open_ports:
                port = port_info['port']
                service_info = {
                    'port': port,
                    'service': common_services.get(port, 'Unknown'),
                    'version': None,
                    'banner': port_info.get('banner'),
                    'confidence': 'high' if port in common_services else 'low'
                }
                
                # Enhanced service detection based on banner
                if service_info['banner']:
                    banner = service_info['banner'].lower()
                    
                    if 'apache' in banner:
                        service_info['service'] = 'Apache HTTP Server'
                        service_info['confidence'] = 'high'
                    elif 'nginx' in banner:
                        service_info['service'] = 'Nginx HTTP Server'
                        service_info['confidence'] = 'high'
                    elif 'microsoft-iis' in banner:
                        service_info['service'] = 'Microsoft IIS'
                        service_info['confidence'] = 'high'
                    elif 'openssh' in banner:
                        service_info['service'] = 'OpenSSH'
                        service_info['confidence'] = 'high'
                
                service_results['services_detected'].append(service_info)
            
        except Exception as e:
            self.log_error(f"Service detection error: {e}")
        
        return service_results
    
    def _detect_os(self, target, **kwargs):
        """Attempt OS detection"""
        os_results = {
            'os_family': None,
            'os_version': None,
            'confidence': 'low',
            'method': 'tcp_fingerprinting'
        }
        
        try:
            # Simple TTL-based OS detection
            if platform.system().lower() != "windows":
                cmd = ["ping", "-c", "1", target]
            else:
                cmd = ["ping", "-n", "1", target]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout
                
                # Extract TTL value
                import re
                ttl_match = re.search(r'ttl=(\d+)', output.lower())
                if ttl_match:
                    ttl = int(ttl_match.group(1))
                    
                    # Common TTL values for OS detection
                    if ttl <= 64:
                        if ttl > 32:
                            os_results['os_family'] = 'Linux/Unix'
                        else:
                            os_results['os_family'] = 'Linux/Unix (Old)'
                    elif ttl <= 128:
                        os_results['os_family'] = 'Windows'
                    elif ttl <= 255:
                        os_results['os_family'] = 'Cisco/Network Device'
                    
                    os_results['confidence'] = 'medium'
            
        except Exception as e:
            self.log_debug(f"OS detection error: {e}")
        
        return os_results
    
    def _analyze_topology(self, target, **kwargs):
        """Analyze network topology"""
        topology_results = {
            'traceroute': [],
            'network_info': {},
            'routing_analysis': {}
        }
        
        try:
            # Perform traceroute
            if platform.system().lower() == "windows":
                cmd = ["tracert", "-h", "10", target]
            else:
                cmd = ["traceroute", "-m", "10", target]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                hops = self._parse_traceroute(result.stdout)
                topology_results['traceroute'] = hops
                topology_results['network_info']['hop_count'] = len(hops)
            
        except Exception as e:
            self.log_debug(f"Topology analysis error: {e}")
        
        return topology_results
    
    def _parse_traceroute(self, output):
        """Parse traceroute output"""
        hops = []
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or 'traceroute' in line.lower():
                continue
            
            # Simple hop extraction
            import re
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
            if ip_match:
                hop_info = {
                    'ip': ip_match.group(1),
                    'hostname': None,
                    'response_time': None
                }
                
                # Extract hostname if present
                hostname_match = re.search(r'([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
                if hostname_match and hostname_match.group(1) != hop_info['ip']:
                    hop_info['hostname'] = hostname_match.group(1)
                
                # Extract response time
                time_match = re.search(r'(\d+(?:\.\d+)?)\s*ms', line)
                if time_match:
                    hop_info['response_time'] = float(time_match.group(1))
                
                hops.append(hop_info)
        
        return hops
    
    def _scan_vulnerabilities(self, target, **kwargs):
        """Basic vulnerability scanning"""
        vuln_results = {
            'vulnerabilities_found': [],
            'security_checks': [],
            'recommendations': []
        }
        
        try:
            # Check for common vulnerable services
            vulnerable_services = {
                21: ['Anonymous FTP', 'Weak FTP configuration'],
                23: ['Telnet (insecure)', 'Unencrypted communication'],
                53: ['DNS amplification', 'Zone transfer'],
                135: ['MS-RPC vulnerable', 'Windows RPC'],
                139: ['NetBIOS vulnerable', 'SMB shares'],
                445: ['SMB vulnerable', 'EternalBlue potential'],
                1433: ['SQL Server default', 'Database exposure'],
                3389: ['RDP exposed', 'Brute force target']
            }
            
            for port_info in self.open_ports:
                if 'port' in port_info:
                    port = port_info['port']
                    if port in vulnerable_services:
                        vuln_info = {
                            'port': port,
                            'service': vulnerable_services[port][0],
                            'risk': vulnerable_services[port][1],
                            'severity': 'medium'
                        }
                        vuln_results['vulnerabilities_found'].append(vuln_info)
            
            # Generate recommendations
            if vuln_results['vulnerabilities_found']:
                vuln_results['recommendations'] = [
                    "Close unnecessary open ports",
                    "Implement proper firewall rules",
                    "Use secure protocols (SSH instead of Telnet)",
                    "Regular security updates and patches",
                    "Network segmentation"
                ]
            
        except Exception as e:
            self.log_error(f"Vulnerability scanning error: {e}")
        
        return vuln_results