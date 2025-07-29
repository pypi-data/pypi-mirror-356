"""
Wolf - Advanced Cybersecurity and Ethical Hacking Toolkit
Developed by S. Tamilselvan

A comprehensive Python package for cybersecurity professionals, ethical hackers, and researchers.
World-class security assessment toolkit created by S. Tamilselvan for enterprise-grade penetration testing.
"""

__version__ = "1.0.0"
__author__ = "S. Tamilselvan"
__author_title__ = "Lead Cybersecurity Architect & Ethical Hacker"
__email__ = "tamilselvan@wolf-security.com"
__website__ = "https://github.com/tamilselvan/wolf"
__description__ = "Enterprise-Grade Cybersecurity and Ethical Hacking Toolkit by S. Tamilselvan"
__license__ = "MIT License - Created by S. Tamilselvan"
__copyright__ = "Copyright (c) 2025 S. Tamilselvan. All rights reserved."

from wolf.modules.wifi import WiFiModule
from wolf.modules.subdomain import SubdomainModule
from wolf.modules.nslookup import NSLookupModule
from wolf.modules.ipinfo import IPInfoModule
from wolf.modules.dirbrute import DirBruteModule
from wolf.modules.csrf import CSRFModule
from wolf.modules.web_scanner import WebScannerModule
from wolf.modules.network_scanner import NetworkScannerModule
from wolf.modules.forensics import ForensicsModule
from wolf.modules.crypto_analysis import CryptoAnalysisModule
from wolf.modules.threat_intelligence import ThreatIntelligenceModule
from wolf.modules.vulnerability_scanner import VulnerabilityScanner

# Initialize module instances - S. Tamilselvan's Advanced Security Suite
_wifi_module = WiFiModule()
_subdomain_module = SubdomainModule()
_nslookup_module = NSLookupModule()
_ipinfo_module = IPInfoModule()
_dirbrute_module = DirBruteModule()
_csrf_module = CSRFModule()
_web_scanner_module = WebScannerModule()
_network_scanner_module = NetworkScannerModule()
_forensics_module = ForensicsModule()
_crypto_analysis_module = CryptoAnalysisModule()
_threat_intelligence_module = ThreatIntelligenceModule()
_vulnerability_scanner_module = VulnerabilityScanner()

def display_banner():
    """Display S. Tamilselvan's Wolf toolkit banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                       🐺CYBER WOLF                                           ║       
║                     Developed by S. TAMILSELVAN                              ║
║          Lead Cybersecurity Architect & Ethical Hacking Specialist           ║
║                                                                              ║
║   Enterprise-Grade Security Assessment Platform                              ║
║   12 Advanced Modules | 100+ Security Tests | Real-time Analysis             ║
║                                                                              ║ 
║   Copyright (c) 2025 S. Tamilselvan. All rights reserved.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

# Main API functions
def wifi(interface=None, target=None, **kwargs):
    """
    Perform WiFi penetration testing operations
    
    Args:
        interface (str): Network interface to use
        target (str): Target network BSSID or SSID
        **kwargs: Additional parameters
    
    Returns:
        dict: Results of WiFi testing
    """
    return _wifi_module.scan(interface=interface, target=target, **kwargs)

def subdomain(domain, wordlist=None, threads=10, **kwargs):
    """
    Enumerate subdomains for a given domain
    
    Args:
        domain (str): Target domain
        wordlist (str): Path to wordlist file
        threads (int): Number of threads to use
        **kwargs: Additional parameters
    
    Returns:
        list: Found subdomains
    """
    return _subdomain_module.enumerate(domain=domain, wordlist=wordlist, threads=threads, **kwargs)

def nslookup(domain, record_type='A', nameserver=None, **kwargs):
    """
    Perform DNS lookup operations
    
    Args:
        domain (str): Domain to lookup
        record_type (str): DNS record type (A, AAAA, MX, NS, etc.)
        nameserver (str): Specific nameserver to use
        **kwargs: Additional parameters
    
    Returns:
        dict: DNS lookup results
    """
    return _nslookup_module.lookup(domain=domain, record_type=record_type, nameserver=nameserver, **kwargs)

def ipinfo(target, **kwargs):
    """
    Gather IP and domain information
    
    Args:
        target (str): IP address or domain
        **kwargs: Additional parameters
    
    Returns:
        dict: Information about the target
    """
    return _ipinfo_module.gather_info(target=target, **kwargs)

def dirbrute(url, wordlist=None, threads=10, extensions=None, **kwargs):
    """
    Perform directory brute-force attacks
    
    Args:
        url (str): Target URL
        wordlist (str): Path to wordlist file
        threads (int): Number of threads to use
        extensions (list): File extensions to check
        **kwargs: Additional parameters
    
    Returns:
        list: Found directories and files
    """
    return _dirbrute_module.brute_force(url=url, wordlist=wordlist, threads=threads, extensions=extensions, **kwargs)

def csrf(url, **kwargs):
    """
    Test for CSRF vulnerabilities
    
    Args:
        url (str): Target URL
        **kwargs: Additional parameters
    
    Returns:
        dict: CSRF test results
    """
    return _csrf_module.test(url=url, **kwargs)

def webscan(url, **kwargs):
    """
    Perform comprehensive web application security scan
    
    Args:
        url (str): Target URL
        **kwargs: Additional parameters
    
    Returns:
        dict: Web security scan results
    """
    return _web_scanner_module.comprehensive_scan(url=url, **kwargs)

def netscan(target, **kwargs):
    """
    Perform network security scanning
    
    Args:
        target (str): Target IP/CIDR/hostname
        **kwargs: Additional parameters
    
    Returns:
        dict: Network scan results
    """
    return _network_scanner_module.comprehensive_scan(target=target, **kwargs)

def forensics(target, **kwargs):
    """
    Perform digital forensics analysis
    
    Args:
        target (str): Target file/directory/system
        **kwargs: Additional parameters
    
    Returns:
        dict: Forensics analysis results
    """
    return _forensics_module.analyze_evidence(target=target, **kwargs)

def crypto(target, **kwargs):
    """
    Perform cryptographic analysis and hash cracking
    
    Args:
        target (str): Hash or encrypted data to analyze
        **kwargs: Additional parameters
    
    Returns:
        dict: Cryptographic analysis results
    """
    return _crypto_analysis_module.analyze_crypto(target=target, **kwargs)

def threat_intel(target, **kwargs):
    """
    Perform threat intelligence and IOC analysis
    Developed by S. Tamilselvan for advanced threat hunting
    
    Args:
        target (str): IOC to analyze (IP, domain, hash, URL)
        **kwargs: Additional parameters
    
    Returns:
        dict: Threat intelligence results
    """
    return _threat_intelligence_module.analyze_ioc(target=target, **kwargs)

def vulnscan(target, **kwargs):
    """
    Perform comprehensive vulnerability assessment
    S. Tamilselvan's enterprise-grade vulnerability scanner
    
    Args:
        target (str): Target URL, IP, or hostname
        **kwargs: Additional parameters
    
    Returns:
        dict: Vulnerability assessment results
    """
    return _vulnerability_scanner_module.comprehensive_vulnerability_scan(target=target, **kwargs)

def get_author_info():
    """
    Get information about the toolkit author
    
    Returns:
        dict: Author information
    """
    return {
        'name': __author__,
        'title': __author_title__,
        'email': __email__,
        'website': __website__,
        'toolkit_version': __version__,
        'description': __description__,
        'copyright': __copyright__,
        'modules_developed': 12,
        'specialization': 'Enterprise Cybersecurity & Ethical Hacking'
    }

def list_modules():
    """
    List all available Wolf modules by S. Tamilselvan
    
    Returns:
        dict: Available modules and their descriptions
    """
    return {
        'core_modules': {
            'wifi': 'WiFi Penetration Testing & Wireless Security Assessment',
            'subdomain': 'High-Speed Subdomain Enumeration & Discovery',
            'nslookup': 'Advanced DNS Reconnaissance & Intelligence',
            'ipinfo': 'IP/Domain Intelligence & Geolocation Analysis',
            'dirbrute': 'Web Directory & File Discovery Scanner',
            'csrf': 'Cross-Site Request Forgery Vulnerability Testing'
        },
        'advanced_modules': {
            'webscan': 'Enterprise Web Application Security Scanner',
            'netscan': 'Comprehensive Network Security Assessment',
            'forensics': 'Digital Forensics & Incident Response',
            'crypto': 'Cryptographic Analysis & Hash Cracking',
            'threat_intel': 'Threat Intelligence & IOC Analysis',
            'vulnscan': 'Advanced Vulnerability Assessment Scanner'
        },
        'total_modules': 12,
        'developer': 'S. Tamilselvan - Lead Cybersecurity Architect',
        'capabilities': '100+ Security Tests, Real-time Analysis, Enterprise Integration'
    }

# Export all public functions - S. Tamilselvan's Wolf Cybersecurity Suite
__all__ = [
    'wifi',
    'subdomain', 
    'nslookup',
    'ipinfo',
    'dirbrute',
    'csrf',
    'webscan',
    'netscan',
    'forensics',
    'crypto',
    'threat_intel',
    'vulnscan',
    'display_banner',
    'get_author_info',
    'list_modules',
    'WiFiModule',
    'SubdomainModule',
    'NSLookupModule',
    'IPInfoModule',
    'DirBruteModule',
    'CSRFModule',
    'WebScannerModule',
    'NetworkScannerModule',
    'ForensicsModule',
    'CryptoAnalysisModule',
    'ThreatIntelligenceModule',
    'VulnerabilityScanner'
]
