"""
DNS lookup module
"""

import socket
import dns.resolver
import dns.reversename
import dns.exception
from wolf.core.base import BaseModule

class NSLookupModule(BaseModule):
    """
    DNS lookup and reconnaissance capabilities
    """
    
    def __init__(self):
        super().__init__("NSLookup")
        self.resolver = dns.resolver.Resolver()
    
    def execute(self, domain, record_type='A', nameserver=None, **kwargs):
        """
        Execute DNS lookup
        
        Args:
            domain (str): Domain to lookup
            record_type (str): DNS record type
            nameserver (str): Specific nameserver
            **kwargs: Additional parameters
            
        Returns:
            dict: DNS lookup results
        """
        return self.lookup(domain=domain, record_type=record_type, nameserver=nameserver, **kwargs)
    
    def lookup(self, domain, record_type='A', nameserver=None, **kwargs):
        """
        Perform DNS lookup
        
        Args:
            domain (str): Domain to lookup
            record_type (str): DNS record type (A, AAAA, MX, NS, CNAME, TXT, SOA)
            nameserver (str): Specific nameserver to use
            **kwargs: Additional parameters
            
        Returns:
            dict: DNS lookup results
        """
        self.log_info(f"Performing DNS lookup for {domain} (type: {record_type})")
        
        # Configure nameserver if specified
        if nameserver:
            self.resolver.nameservers = [nameserver]
        
        results = {
            'domain': domain,
            'record_type': record_type,
            'nameserver': nameserver or 'default',
            'records': [],
            'additional_info': {}
        }
        
        try:
            # Perform the DNS query
            answers = self.resolver.resolve(domain, record_type)
            
            for answer in answers:
                record_data = {
                    'data': str(answer),
                    'ttl': answers.rrset.ttl if hasattr(answers, 'rrset') else 'N/A'
                }
                
                # Add record-specific information
                if record_type == 'MX':
                    record_data['preference'] = answer.preference
                    record_data['exchange'] = str(answer.exchange)
                elif record_type == 'SOA':
                    record_data['mname'] = str(answer.mname)
                    record_data['rname'] = str(answer.rname)
                    record_data['serial'] = answer.serial
                    record_data['refresh'] = answer.refresh
                    record_data['retry'] = answer.retry
                    record_data['expire'] = answer.expire
                    record_data['minimum'] = answer.minimum
                
                results['records'].append(record_data)
            
            self.log_info(f"Found {len(results['records'])} {record_type} records for {domain}")
            
        except dns.resolver.NXDOMAIN:
            self.log_warning(f"Domain {domain} does not exist")
            results['error'] = 'Domain not found'
        except dns.resolver.NoAnswer:
            self.log_warning(f"No {record_type} records found for {domain}")
            results['error'] = f'No {record_type} records found'
        except dns.exception.Timeout:
            self.log_error(f"DNS query timeout for {domain}")
            results['error'] = 'Query timeout'
        except Exception as e:
            self.log_error(f"DNS lookup error: {e}")
            results['error'] = str(e)
        
        return results
    
    def reverse_lookup(self, ip_address, **kwargs):
        """
        Perform reverse DNS lookup
        
        Args:
            ip_address (str): IP address to lookup
            **kwargs: Additional parameters
            
        Returns:
            dict: Reverse lookup results
        """
        self.log_info(f"Performing reverse DNS lookup for {ip_address}")
        
        results = {
            'ip_address': ip_address,
            'hostnames': [],
            'error': None
        }
        
        try:
            # Create reverse DNS name
            reverse_name = dns.reversename.from_address(ip_address)
            
            # Perform reverse lookup
            answers = self.resolver.resolve(reverse_name, 'PTR')
            
            for answer in answers:
                results['hostnames'].append(str(answer))
            
            self.log_info(f"Found {len(results['hostnames'])} hostnames for {ip_address}")
            
        except dns.resolver.NXDOMAIN:
            self.log_warning(f"No reverse DNS record for {ip_address}")
            results['error'] = 'No reverse DNS record found'
        except dns.exception.Timeout:
            self.log_error(f"Reverse DNS query timeout for {ip_address}")
            results['error'] = 'Query timeout'
        except Exception as e:
            self.log_error(f"Reverse DNS lookup error: {e}")
            results['error'] = str(e)
        
        return results
    
    def zone_transfer(self, domain, nameserver=None, **kwargs):
        """
        Attempt DNS zone transfer
        
        Args:
            domain (str): Domain for zone transfer
            nameserver (str): Nameserver to query
            **kwargs: Additional parameters
            
        Returns:
            dict: Zone transfer results
        """
        self.log_info(f"Attempting zone transfer for {domain}")
        
        results = {
            'domain': domain,
            'nameserver': nameserver,
            'records': [],
            'success': False,
            'error': None
        }
        
        try:
            # Get nameservers if not specified
            if not nameserver:
                ns_records = self.lookup(domain, 'NS')
                if ns_records.get('records'):
                    nameserver = ns_records['records'][0]['data']
                else:
                    results['error'] = 'No nameservers found'
                    return results
            
            # Attempt zone transfer
            zone = dns.zone.from_xfr(dns.query.xfr(nameserver, domain))
            
            for name, node in zone.nodes.items():
                for rdataset in node.rdatasets:
                    for rdata in rdataset:
                        record = {
                            'name': str(name),
                            'type': dns.rdatatype.to_text(rdataset.rdtype),
                            'data': str(rdata),
                            'ttl': rdataset.ttl
                        }
                        results['records'].append(record)
            
            results['success'] = True
            self.log_info(f"Zone transfer successful: {len(results['records'])} records")
            
        except dns.exception.FormError:
            self.log_warning(f"Zone transfer refused for {domain}")
            results['error'] = 'Zone transfer refused'
        except Exception as e:
            self.log_error(f"Zone transfer error: {e}")
            results['error'] = str(e)
        
        return results
    
    def comprehensive_lookup(self, domain, **kwargs):
        """
        Perform comprehensive DNS lookup with multiple record types
        
        Args:
            domain (str): Domain to lookup
            **kwargs: Additional parameters
            
        Returns:
            dict: Comprehensive lookup results
        """
        self.log_info(f"Performing comprehensive DNS lookup for {domain}")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'CNAME', 'TXT', 'SOA']
        results = {
            'domain': domain,
            'records': {},
            'summary': {
                'total_records': 0,
                'record_types_found': []
            }
        }
        
        for record_type in record_types:
            lookup_result = self.lookup(domain, record_type)
            results['records'][record_type] = lookup_result
            
            if lookup_result.get('records') and not lookup_result.get('error'):
                results['summary']['total_records'] += len(lookup_result['records'])
                results['summary']['record_types_found'].append(record_type)
        
        self.log_info(f"Comprehensive lookup complete: {results['summary']['total_records']} total records")
        return results
