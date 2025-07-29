"""
WiFi penetration testing module
"""

import subprocess
import re
import os
import time
from wolf.core.base import BaseModule

class WiFiModule(BaseModule):
    """
    WiFi penetration testing capabilities
    """
    
    def __init__(self):
        super().__init__("WiFi")
        self.interfaces = []
        self.networks = []
    
    def _setup(self):
        """Setup WiFi module"""
        self.log_info("Initializing WiFi module")
        self._check_requirements()
    
    def _check_requirements(self):
        """Check if required tools are available"""
        tools = ['iwconfig', 'airmon-ng', 'airodump-ng']
        missing_tools = []
        
        for tool in tools:
            try:
                subprocess.run([tool, '--help'], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing_tools.append(tool)
        
        if missing_tools:
            self.log_warning(f"Missing tools: {', '.join(missing_tools)}")
            self.log_warning("Some WiFi features may not work properly")
    
    def execute(self, interface=None, target=None, **kwargs):
        """
        Execute WiFi operations
        
        Args:
            interface (str): Network interface
            target (str): Target network
            **kwargs: Additional parameters
            
        Returns:
            dict: Results
        """
        return self.scan(interface=interface, target=target, **kwargs)
    
    def scan(self, interface=None, target=None, duration=30, **kwargs):
        """
        Scan for WiFi networks
        
        Args:
            interface (str): Network interface to use
            target (str): Specific target to focus on
            duration (int): Scan duration in seconds
            **kwargs: Additional parameters
            
        Returns:
            dict: Scan results
        """
        self.log_info("Starting WiFi scan")
        
        if not interface:
            interface = self._get_wireless_interface()
            if not interface:
                self.log_error("No wireless interface found")
                return {"error": "No wireless interface available"}
        
        try:
            # Get available networks using iwlist
            result = subprocess.run(
                ['iwlist', interface, 'scan'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            networks = self._parse_iwlist_output(result.stdout)
            
            self.log_info(f"Found {len(networks)} networks")
            
            return {
                "interface": interface,
                "networks": networks,
                "scan_duration": duration,
                "timestamp": time.time()
            }
            
        except subprocess.TimeoutExpired:
            self.log_error("WiFi scan timed out")
            return {"error": "Scan timeout"}
        except subprocess.CalledProcessError as e:
            self.log_error(f"WiFi scan failed: {e}")
            return {"error": f"Scan failed: {e}"}
        except Exception as e:
            self.log_error(f"Unexpected error during WiFi scan: {e}")
            return {"error": f"Unexpected error: {e}"}
    
    def _get_wireless_interface(self):
        """
        Get available wireless interface
        
        Returns:
            str: Interface name or None
        """
        try:
            result = subprocess.run(
                ['iwconfig'],
                capture_output=True,
                text=True
            )
            
            # Parse iwconfig output to find wireless interfaces
            interfaces = re.findall(r'^(\w+)\s+IEEE 802.11', result.stdout, re.MULTILINE)
            
            if interfaces:
                return interfaces[0]
            
            # Fallback: check common interface names
            common_interfaces = ['wlan0', 'wlan1', 'wlp2s0', 'wlp3s0']
            for iface in common_interfaces:
                if os.path.exists(f'/sys/class/net/{iface}'):
                    return iface
            
            return None
            
        except Exception as e:
            self.log_error(f"Error getting wireless interface: {e}")
            return None
    
    def _parse_iwlist_output(self, output):
        """
        Parse iwlist scan output
        
        Args:
            output (str): iwlist output
            
        Returns:
            list: Parsed network information
        """
        networks = []
        current_network = {}
        
        for line in output.split('\n'):
            line = line.strip()
            
            if 'Cell' in line and 'Address:' in line:
                if current_network:
                    networks.append(current_network)
                current_network = {
                    'bssid': re.search(r'Address: ([A-Fa-f0-9:]{17})', line).group(1) if re.search(r'Address: ([A-Fa-f0-9:]{17})', line) else 'Unknown'
                }
            
            elif 'ESSID:' in line:
                essid_match = re.search(r'ESSID:"([^"]*)"', line)
                current_network['ssid'] = essid_match.group(1) if essid_match else 'Hidden'
            
            elif 'Quality=' in line:
                quality_match = re.search(r'Quality=(\d+/\d+)', line)
                signal_match = re.search(r'Signal level=(-?\d+)', line)
                current_network['quality'] = quality_match.group(1) if quality_match else 'Unknown'
                current_network['signal'] = signal_match.group(1) if signal_match else 'Unknown'
            
            elif 'Encryption key:' in line:
                current_network['encrypted'] = 'on' in line.lower()
            
            elif 'IE: IEEE 802.11i/WPA2' in line:
                current_network['security'] = 'WPA2'
            elif 'IE: WPA' in line:
                current_network['security'] = 'WPA'
            elif not current_network.get('security') and current_network.get('encrypted'):
                current_network['security'] = 'WEP'
            elif not current_network.get('security'):
                current_network['security'] = 'Open'
        
        if current_network:
            networks.append(current_network)
        
        return networks
    
    def monitor_mode(self, interface, enable=True):
        """
        Enable/disable monitor mode on interface
        
        Args:
            interface (str): Network interface
            enable (bool): True to enable, False to disable
            
        Returns:
            dict: Operation result
        """
        try:
            if enable:
                self.log_info(f"Enabling monitor mode on {interface}")
                subprocess.run(['airmon-ng', 'start', interface], check=True)
                return {"status": "success", "message": f"Monitor mode enabled on {interface}"}
            else:
                self.log_info(f"Disabling monitor mode on {interface}")
                subprocess.run(['airmon-ng', 'stop', interface], check=True)
                return {"status": "success", "message": f"Monitor mode disabled on {interface}"}
                
        except subprocess.CalledProcessError as e:
            self.log_error(f"Failed to change monitor mode: {e}")
            return {"status": "error", "message": f"Monitor mode operation failed: {e}"}
        except FileNotFoundError:
            self.log_error("airmon-ng not found")
            return {"status": "error", "message": "airmon-ng tool not available"}
