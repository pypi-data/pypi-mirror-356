"""
Directory brute-force attack module
"""

import requests
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
from wolf.core.base import BaseModule
from wolf.utils.wordlists import get_directory_wordlist

class DirBruteModule(BaseModule):
    """
    Directory and file brute-force capabilities
    """
    
    def __init__(self):
        super().__init__("DirBrute")
        self.found_paths = []
        self.lock = threading.Lock()
        self.session = requests.Session()
        # Set common headers to appear more legitimate
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def execute(self, url, wordlist=None, threads=10, extensions=None, **kwargs):
        """
        Execute directory brute-force
        
        Args:
            url (str): Target URL
            wordlist (str): Wordlist file path
            threads (int): Number of threads
            extensions (list): File extensions to check
            **kwargs: Additional parameters
            
        Returns:
            list: Found directories and files
        """
        return self.brute_force(url=url, wordlist=wordlist, threads=threads, extensions=extensions, **kwargs)
    
    def brute_force(self, url, wordlist=None, threads=10, extensions=None, 
                   status_codes=None, timeout=10, **kwargs):
        """
        Perform directory brute-force attack
        
        Args:
            url (str): Target URL
            wordlist (str): Path to wordlist file
            threads (int): Number of threads to use
            extensions (list): File extensions to check
            status_codes (list): HTTP status codes to consider as found
            timeout (int): Request timeout
            **kwargs: Additional parameters
            
        Returns:
            list: Found directories and files
        """
        self.log_info(f"Starting directory brute-force on {url}")
        
        # Validate URL
        if not self._validate_url(url):
            self.log_error(f"Invalid URL: {url}")
            return []
        
        # Ensure URL ends with /
        if not url.endswith('/'):
            url += '/'
        
        # Get wordlist
        if wordlist:
            words = self._load_wordlist(wordlist)
        else:
            words = get_directory_wordlist()
        
        if not words:
            self.log_error("No wordlist available")
            return []
        
        # Set default extensions and status codes
        if extensions is None:
            extensions = ['', '.php', '.html', '.htm', '.asp', '.aspx', '.jsp', '.txt', '.js', '.css']
        
        if status_codes is None:
            status_codes = [200, 301, 302, 403, 401]
        
        # Generate all possible paths
        paths_to_test = []
        for word in words:
            for ext in extensions:
                paths_to_test.append(word + ext)
        
        self.found_paths = []
        self.log_info(f"Testing {len(paths_to_test)} paths with {threads} threads")
        
        # Perform baseline request to detect differences
        baseline_response = self._get_baseline_response(url, timeout)
        
        # Use ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for path in paths_to_test:
                full_url = urljoin(url, path)
                future = executor.submit(
                    self._check_path, 
                    full_url, 
                    path, 
                    status_codes, 
                    timeout, 
                    baseline_response
                )
                futures.append(future)
            
            # Wait for all futures to complete
            for future in futures:
                try:
                    future.result(timeout=timeout + 1)
                except Exception as e:
                    self.log_debug(f"Thread error: {e}")
        
        self.log_info(f"Found {len(self.found_paths)} accessible paths")
        return sorted(self.found_paths, key=lambda x: x['path'])
    
    def _validate_url(self, url):
        """
        Validate URL format
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
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
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            self.log_error(f"Wordlist file not found: {wordlist_path}")
            return []
        except Exception as e:
            self.log_error(f"Error loading wordlist: {e}")
            return []
    
    def _get_baseline_response(self, url, timeout):
        """
        Get baseline response for comparison
        
        Args:
            url (str): Base URL
            timeout (int): Request timeout
            
        Returns:
            dict: Baseline response information
        """
        try:
            # Test with a random non-existent path
            test_path = urljoin(url, 'wolf_test_nonexistent_path_12345')
            response = self.session.get(test_path, timeout=timeout, allow_redirects=False)
            
            return {
                'status_code': response.status_code,
                'content_length': len(response.content),
                'headers': dict(response.headers)
            }
        except Exception as e:
            self.log_debug(f"Error getting baseline response: {e}")
            return {'status_code': 404, 'content_length': 0, 'headers': {}}
    
    def _check_path(self, full_url, path, status_codes, timeout, baseline_response):
        """
        Check if a path exists
        
        Args:
            full_url (str): Full URL to check
            path (str): Relative path
            status_codes (list): Status codes to consider as found
            timeout (int): Request timeout
            baseline_response (dict): Baseline response for comparison
        """
        try:
            response = self.session.get(
                full_url,
                timeout=timeout,
                allow_redirects=False,
                verify=False
            )
            
            # Check if response indicates a found resource
            if self._is_valid_response(response, baseline_response, status_codes):
                path_info = {
                    'path': path,
                    'url': full_url,
                    'status_code': response.status_code,
                    'content_length': len(response.content),
                    'content_type': response.headers.get('Content-Type', 'Unknown'),
                    'server': response.headers.get('Server', 'Unknown')
                }
                
                # Add redirect information if applicable
                if response.status_code in [301, 302, 307, 308]:
                    path_info['redirect_location'] = response.headers.get('Location', 'Unknown')
                
                with self.lock:
                    self.found_paths.append(path_info)
                    self.log_info(f"Found: {path} ({response.status_code})")
            
        except requests.exceptions.Timeout:
            self.log_debug(f"Timeout for {path}")
        except requests.exceptions.ConnectionError:
            self.log_debug(f"Connection error for {path}")
        except Exception as e:
            self.log_debug(f"Error checking {path}: {e}")
    
    def _is_valid_response(self, response, baseline_response, status_codes):
        """
        Determine if response indicates a valid resource
        
        Args:
            response (requests.Response): Response to check
            baseline_response (dict): Baseline response
            status_codes (list): Valid status codes
            
        Returns:
            bool: True if response indicates found resource
        """
        # Check status code
        if response.status_code not in status_codes:
            return False
        
        # Avoid false positives by comparing with baseline
        if (response.status_code == baseline_response['status_code'] and
            abs(len(response.content) - baseline_response['content_length']) < 100):
            return False
        
        return True
    
    def recursive_brute_force(self, url, max_depth=2, **kwargs):
        """
        Perform recursive directory brute-force
        
        Args:
            url (str): Target URL
            max_depth (int): Maximum recursion depth
            **kwargs: Additional parameters
            
        Returns:
            list: All found paths including recursive discoveries
        """
        self.log_info(f"Starting recursive brute-force (max depth: {max_depth})")
        
        all_found = []
        processed_urls = set()
        
        def recursive_scan(current_url, depth):
            if depth > max_depth or current_url in processed_urls:
                return
            
            processed_urls.add(current_url)
            found_paths = self.brute_force(current_url, **kwargs)
            all_found.extend(found_paths)
            
            # Recursively scan found directories
            for path_info in found_paths:
                if (path_info['status_code'] in [200, 301, 302] and 
                    not any(ext in path_info['path'] for ext in ['.php', '.html', '.htm', '.txt', '.js', '.css'])):
                    # This looks like a directory
                    new_url = path_info['url']
                    if not new_url.endswith('/'):
                        new_url += '/'
                    recursive_scan(new_url, depth + 1)
        
        recursive_scan(url, 0)
        
        self.log_info(f"Recursive scan complete: {len(all_found)} total paths found")
        return all_found
    
    def custom_scan(self, url, custom_paths, **kwargs):
        """
        Scan for custom list of paths
        
        Args:
            url (str): Target URL
            custom_paths (list): Custom paths to check
            **kwargs: Additional parameters
            
        Returns:
            list: Found paths
        """
        self.log_info(f"Starting custom path scan on {url}")
        
        if not custom_paths:
            self.log_error("No custom paths provided")
            return []
        
        self.found_paths = []
        timeout = kwargs.get('timeout', 10)
        status_codes = kwargs.get('status_codes', [200, 301, 302, 403, 401])
        baseline_response = self._get_baseline_response(url, timeout)
        
        for path in custom_paths:
            full_url = urljoin(url, path)
            self._check_path(full_url, path, status_codes, timeout, baseline_response)
        
        return self.found_paths
