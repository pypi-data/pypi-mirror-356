"""
Wolf cybersecurity modules
"""

from wolf.modules.wifi import WiFiModule
from wolf.modules.subdomain import SubdomainModule
from wolf.modules.nslookup import NSLookupModule
from wolf.modules.ipinfo import IPInfoModule
from wolf.modules.dirbrute import DirBruteModule
from wolf.modules.csrf import CSRFModule

__all__ = [
    'WiFiModule',
    'SubdomainModule',
    'NSLookupModule',
    'IPInfoModule',
    'DirBruteModule',
    'CSRFModule'
]
