"""
IP and domain information gathering module
"""

import requests
import socket
import ipaddress
import whois
import json
from wolf.core.base import BaseModule

class IPInfoModule(BaseModule):
    """
    IP and domain information gathering capabilities
    """
    
    def __init__(self):
        super().__init__("IPInfo")
        self.api_key = None
    
    def execute(self, target, **kwargs):
        """
        Execute IP information gathering
        
        Args:
            target (str): IP address or domain
            **kwargs: Additional parameters
            
        Returns:
            dict: Information about the target
        """
        return self.gather_info(target=target, **kwargs)
    
    def gather_info(self, target, include_geolocation=True, include_whois=True, **kwargs):
        """
        Gather comprehensive information about IP or domain
        
        Args:
            target (str): IP address or domain name
            include_geolocation (bool): Include geolocation data
            include_whois (bool): Include WHOIS data
            **kwargs: Additional parameters
            
        Returns:
            dict: Comprehensive target information
        """
        self.log_info(f"Gathering information for {target}")
        
        results = {
            'target': target,
            'target_type': self._determine_target_type(target),
            'basic_info': {},
            'geolocation': {},
            'whois': {},
            'network_info': {},
            'security_info': {},
            'error': None
        }
        
        try:
            # Get basic information
            results['basic_info'] = self._get_basic_info(target)
            
            # Get IP address if target is domain
            ip_address = self._resolve_to_ip(target)
            if ip_address:
                results['basic_info']['resolved_ip'] = ip_address
                
                # Get geolocation information
                if include_geolocation:
                    results['geolocation'] = self._get_geolocation(ip_address)
                
                # Get network information
                results['network_info'] = self._get_network_info(ip_address)
            
            # Get WHOIS information
            if include_whois:
                results['whois'] = self._get_whois_info(target)
            
            # Get security-related information
            results['security_info'] = self._get_security_info(target)
            
        except Exception as e:
            self.log_error(f"Error gathering information: {e}")
            results['error'] = str(e)
        
        return results
    
    def _determine_target_type(self, target):
        """
        Determine if target is IP address or domain
        
        Args:
            target (str): Target to analyze
            
        Returns:
            str: 'ip' or 'domain'
        """
        try:
            ipaddress.ip_address(target)
            return 'ip'
        except ValueError:
            return 'domain'
    
    def _get_basic_info(self, target):
        """
        Get basic information about target
        
        Args:
            target (str): Target to analyze
            
        Returns:
            dict: Basic information
        """
        info = {
            'target': target,
            'type': self._determine_target_type(target)
        }
        
        if info['type'] == 'ip':
            try:
                ip_obj = ipaddress.ip_address(target)
                info['version'] = ip_obj.version
                info['is_private'] = ip_obj.is_private
                info['is_loopback'] = ip_obj.is_loopback
                info['is_multicast'] = ip_obj.is_multicast
            except Exception as e:
                self.log_debug(f"Error analyzing IP: {e}")
        
        return info
    
    def _resolve_to_ip(self, target):
        """
        Resolve domain to IP address
        
        Args:
            target (str): Domain or IP
            
        Returns:
            str: IP address or None
        """
        try:
            if self._determine_target_type(target) == 'ip':
                return target
            else:
                return socket.gethostbyname(target)
        except Exception as e:
            self.log_debug(f"Error resolving {target}: {e}")
            return None
    
    def _get_geolocation(self, ip_address):
        """
        Get geolocation information for IP
        
        Args:
            ip_address (str): IP address
            
        Returns:
            dict: Geolocation information
        """
        geolocation = {}
        
        try:
            # Try multiple free geolocation services
            services = [
                f"http://ip-api.com/json/{ip_address}",
                f"https://ipapi.co/{ip_address}/json/",
                f"http://ipinfo.io/{ip_address}/json"
            ]
            
            for service_url in services:
                try:
                    response = requests.get(service_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Normalize data from different services
                        if 'ip-api.com' in service_url:
                            geolocation = {
                                'ip': data.get('query'),
                                'country': data.get('country'),
                                'country_code': data.get('countryCode'),
                                'region': data.get('regionName'),
                                'city': data.get('city'),
                                'latitude': data.get('lat'),
                                'longitude': data.get('lon'),
                                'timezone': data.get('timezone'),
                                'isp': data.get('isp'),
                                'org': data.get('org'),
                                'as': data.get('as')
                            }
                        elif 'ipapi.co' in service_url:
                            geolocation = {
                                'ip': data.get('ip'),
                                'country': data.get('country_name'),
                                'country_code': data.get('country'),
                                'region': data.get('region'),
                                'city': data.get('city'),
                                'latitude': data.get('latitude'),
                                'longitude': data.get('longitude'),
                                'timezone': data.get('timezone'),
                                'isp': data.get('org')
                            }
                        elif 'ipinfo.io' in service_url:
                            geolocation = {
                                'ip': data.get('ip'),
                                'country': data.get('country'),
                                'region': data.get('region'),
                                'city': data.get('city'),
                                'location': data.get('loc'),
                                'timezone': data.get('timezone'),
                                'isp': data.get('org')
                            }
                        
                        if geolocation:
                            break
                            
                except Exception as e:
                    self.log_debug(f"Geolocation service error: {e}")
                    continue
            
        except Exception as e:
            self.log_error(f"Error getting geolocation: {e}")
        
        return geolocation
    
    def _get_whois_info(self, target):
        """
        Get WHOIS information
        
        Args:
            target (str): Domain or IP
            
        Returns:
            dict: WHOIS information
        """
        whois_info = {}
        
        try:
            if self._determine_target_type(target) == 'domain':
                w = whois.whois(target)
                whois_info = {
                    'domain_name': w.domain_name,
                    'registrar': w.registrar,
                    'creation_date': str(w.creation_date) if w.creation_date else None,
                    'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                    'updated_date': str(w.updated_date) if w.updated_date else None,
                    'name_servers': w.name_servers,
                    'status': w.status,
                    'emails': w.emails,
                    'org': w.org,
                    'country': w.country
                }
            else:
                # For IP addresses, we can use online WHOIS services
                whois_info = self._get_ip_whois(target)
                
        except Exception as e:
            self.log_error(f"Error getting WHOIS info: {e}")
            whois_info['error'] = str(e)
        
        return whois_info
    
    def _get_ip_whois(self, ip_address):
        """
        Get WHOIS information for IP address
        
        Args:
            ip_address (str): IP address
            
        Returns:
            dict: IP WHOIS information
        """
        try:
            # Use a free IP WHOIS service
            response = requests.get(
                f"http://ipwhois.app/json/{ip_address}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'ip': data.get('ip'),
                    'success': data.get('success'),
                    'type': data.get('type'),
                    'continent': data.get('continent'),
                    'country': data.get('country'),
                    'region': data.get('region'),
                    'city': data.get('city'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'isp': data.get('isp'),
                    'org': data.get('org'),
                    'as': data.get('as'),
                    'asname': data.get('asname')
                }
        except Exception as e:
            self.log_debug(f"IP WHOIS error: {e}")
        
        return {}
    
    def _get_network_info(self, ip_address):
        """
        Get network information for IP
        
        Args:
            ip_address (str): IP address
            
        Returns:
            dict: Network information
        """
        network_info = {}
        
        try:
            # Port scanning information (basic)
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
            open_ports = []
            
            for port in common_ports:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((ip_address, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            
            network_info['open_ports'] = open_ports
            
            # Get hostname
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                network_info['hostname'] = hostname
            except:
                network_info['hostname'] = None
            
        except Exception as e:
            self.log_error(f"Error getting network info: {e}")
        
        return network_info
    
    def _get_security_info(self, target):
        """
        Get security-related information
        
        Args:
            target (str): Target to analyze
            
        Returns:
            dict: Security information
        """
        security_info = {}
        
        try:
            # Check if it's a web service
            if self._determine_target_type(target) == 'domain':
                security_info.update(self._check_web_security(target))
            
            # Add reputation check (placeholder)
            security_info['reputation_check'] = 'Not implemented'
            
        except Exception as e:
            self.log_error(f"Error getting security info: {e}")
        
        return security_info
    
    def _check_web_security(self, domain):
        """
        Check web security headers and SSL
        
        Args:
            domain (str): Domain to check
            
        Returns:
            dict: Web security information
        """
        security_info = {}
        
        try:
            for protocol in ['https', 'http']:
                url = f"{protocol}://{domain}"
                try:
                    response = requests.get(url, timeout=10, verify=False)
                    security_info[f'{protocol}_status_code'] = response.status_code
                    security_info[f'{protocol}_headers'] = dict(response.headers)
                    break
                except:
                    continue
            
        except Exception as e:
            self.log_debug(f"Web security check error: {e}")
        
        return security_info
