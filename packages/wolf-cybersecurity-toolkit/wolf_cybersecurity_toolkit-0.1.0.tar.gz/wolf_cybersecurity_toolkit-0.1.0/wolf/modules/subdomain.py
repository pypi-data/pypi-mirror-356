"""
Subdomain enumeration module
"""

import requests
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from wolf.core.base import BaseModule
from wolf.utils.wordlists import get_subdomain_wordlist

class SubdomainModule(BaseModule):
    """
    Subdomain enumeration capabilities
    """
    
    def __init__(self):
        super().__init__("Subdomain")
        self.found_subdomains = []
        self.lock = threading.Lock()
    
    def execute(self, domain, wordlist=None, threads=10, **kwargs):
        """
        Execute subdomain enumeration
        
        Args:
            domain (str): Target domain
            wordlist (str): Wordlist file path
            threads (int): Number of threads
            **kwargs: Additional parameters
            
        Returns:
            list: Found subdomains
        """
        return self.enumerate(domain=domain, wordlist=wordlist, threads=threads, **kwargs)
    
    def enumerate(self, domain, wordlist=None, threads=10, timeout=5, **kwargs):
        """
        Enumerate subdomains for a domain
        
        Args:
            domain (str): Target domain
            wordlist (str): Path to wordlist file
            threads (int): Number of threads to use
            timeout (int): Request timeout
            **kwargs: Additional parameters
            
        Returns:
            list: Found subdomains
        """
        self.log_info(f"Starting subdomain enumeration for {domain}")
        
        if not self._validate_domain(domain):
            self.log_error(f"Invalid domain: {domain}")
            return []
        
        # Get wordlist
        if wordlist:
            subdomains = self._load_wordlist(wordlist)
        else:
            subdomains = get_subdomain_wordlist()
        
        if not subdomains:
            self.log_error("No wordlist available")
            return []
        
        self.found_subdomains = []
        self.log_info(f"Testing {len(subdomains)} subdomains with {threads} threads")
        
        # Use ThreadPoolExecutor for concurrent subdomain checking
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for subdomain in subdomains:
                full_domain = f"{subdomain}.{domain}"
                future = executor.submit(self._check_subdomain, full_domain, timeout)
                futures.append(future)
            
            # Wait for all futures to complete
            for future in futures:
                try:
                    future.result(timeout=timeout + 1)
                except Exception as e:
                    self.log_debug(f"Thread error: {e}")
        
        self.log_info(f"Found {len(self.found_subdomains)} subdomains")
        return sorted(list(set(self.found_subdomains)))
    
    def _validate_domain(self, domain):
        """
        Validate domain format
        
        Args:
            domain (str): Domain to validate
            
        Returns:
            bool: True if valid
        """
        import re
        pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))
    
    def _load_wordlist(self, wordlist_path):
        """
        Load wordlist from file
        
        Args:
            wordlist_path (str): Path to wordlist file
            
        Returns:
            list: Wordlist entries
        """
        try:
            with open(wordlist_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.log_error(f"Wordlist file not found: {wordlist_path}")
            return []
        except Exception as e:
            self.log_error(f"Error loading wordlist: {e}")
            return []
    
    def _check_subdomain(self, subdomain, timeout):
        """
        Check if subdomain exists
        
        Args:
            subdomain (str): Subdomain to check
            timeout (int): Request timeout
        """
        try:
            # DNS resolution check
            socket.gethostbyname(subdomain)
            
            with self.lock:
                self.found_subdomains.append(subdomain)
                self.log_info(f"Found: {subdomain}")
            
            # Additional HTTP check
            self._check_http_response(subdomain, timeout)
            
        except socket.gaierror:
            # Subdomain doesn't exist
            pass
        except Exception as e:
            self.log_debug(f"Error checking {subdomain}: {e}")
    
    def _check_http_response(self, subdomain, timeout):
        """
        Check HTTP response for subdomain
        
        Args:
            subdomain (str): Subdomain to check
            timeout (int): Request timeout
        """
        try:
            for protocol in ['https', 'http']:
                url = f"{protocol}://{subdomain}"
                response = requests.get(
                    url,
                    timeout=timeout,
                    verify=False,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    self.log_debug(f"{subdomain} - HTTP {response.status_code}")
                    break
                    
        except requests.exceptions.RequestException:
            # HTTP check failed, but DNS resolution succeeded
            pass
    
    def brute_force_dns(self, domain, custom_nameservers=None, **kwargs):
        """
        Perform DNS brute force with custom nameservers
        
        Args:
            domain (str): Target domain
            custom_nameservers (list): Custom DNS servers to use
            **kwargs: Additional parameters
            
        Returns:
            list: Found subdomains
        """
        self.log_info(f"Starting DNS brute force for {domain}")
        
        if custom_nameservers:
            # Configure custom nameservers
            original_nameservers = self._get_system_nameservers()
            self._set_nameservers(custom_nameservers)
        
        try:
            result = self.enumerate(domain, **kwargs)
        finally:
            if custom_nameservers:
                # Restore original nameservers
                self._set_nameservers(original_nameservers)
        
        return result
    
    def _get_system_nameservers(self):
        """Get current system nameservers"""
        try:
            with open('/etc/resolv.conf', 'r') as f:
                nameservers = []
                for line in f:
                    if line.startswith('nameserver'):
                        nameservers.append(line.split()[1])
                return nameservers
        except Exception:
            return ['8.8.8.8', '8.8.4.4']  # Default to Google DNS
    
    def _set_nameservers(self, nameservers):
        """Set custom nameservers (requires root privileges)"""
        # Note: This would require root privileges in a real implementation
        self.log_warning("Custom nameserver configuration requires root privileges")
