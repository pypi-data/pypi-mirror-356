"""
Network utility functions
"""

import socket
import ipaddress
import requests
from urllib.parse import urlparse

class NetworkUtils:
    """
    Network utility functions for Wolf toolkit
    """
    
    @staticmethod
    def is_valid_ip(ip_string):
        """
        Check if string is a valid IP address
        
        Args:
            ip_string (str): String to check
            
        Returns:
            bool: True if valid IP address
        """
        try:
            ipaddress.ip_address(ip_string)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_domain(domain):
        """
        Check if string is a valid domain name
        
        Args:
            domain (str): Domain to check
            
        Returns:
            bool: True if valid domain
        """
        import re
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))
    
    @staticmethod
    def resolve_domain(domain):
        """
        Resolve domain to IP address
        
        Args:
            domain (str): Domain to resolve
            
        Returns:
            str: IP address or None
        """
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            return None
    
    @staticmethod
    def reverse_dns_lookup(ip_address):
        """
        Perform reverse DNS lookup
        
        Args:
            ip_address (str): IP address
            
        Returns:
            str: Hostname or None
        """
        try:
            return socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            return None
    
    @staticmethod
    def check_port(host, port, timeout=3):
        """
        Check if port is open on host
        
        Args:
            host (str): Host to check
            port (int): Port to check
            timeout (int): Connection timeout
            
        Returns:
            bool: True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    @staticmethod
    def get_http_headers(url, timeout=10):
        """
        Get HTTP headers for URL
        
        Args:
            url (str): URL to check
            timeout (int): Request timeout
            
        Returns:
            dict: HTTP headers or None
        """
        try:
            response = requests.head(url, timeout=timeout, verify=False)
            return dict(response.headers)
        except Exception:
            return None
    
    @staticmethod
    def parse_url(url):
        """
        Parse URL into components
        
        Args:
            url (str): URL to parse
            
        Returns:
            dict: URL components
        """
        try:
            parsed = urlparse(url)
            return {
                'scheme': parsed.scheme,
                'netloc': parsed.netloc,
                'hostname': parsed.hostname,
                'port': parsed.port,
                'path': parsed.path,
                'params': parsed.params,
                'query': parsed.query,
                'fragment': parsed.fragment
            }
        except Exception:
            return {}
    
    @staticmethod
    def get_local_ip():
        """
        Get local IP address
        
        Returns:
            str: Local IP address
        """
        try:
            # Connect to a remote server to determine local IP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            local_ip = sock.getsockname()[0]
            sock.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def get_network_interfaces():
        """
        Get available network interfaces
        
        Returns:
            list: Network interface names
        """
        import os
        interfaces = []
        
        try:
            # Linux/Unix systems
            for interface in os.listdir('/sys/class/net/'):
                if interface != 'lo':  # Skip loopback
                    interfaces.append(interface)
        except Exception:
            # Fallback for other systems
            interfaces = ['eth0', 'wlan0', 'en0', 'wlp2s0']
        
        return interfaces
    
    @staticmethod
    def ping_host(host, timeout=3):
        """
        Ping host to check connectivity
        
        Args:
            host (str): Host to ping
            timeout (int): Ping timeout
            
        Returns:
            bool: True if host is reachable
        """
        import subprocess
        import platform
        
        try:
            # Determine ping command based on OS
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
            else:
                cmd = ["ping", "-c", "1", "-W", str(timeout), host]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout + 1
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
