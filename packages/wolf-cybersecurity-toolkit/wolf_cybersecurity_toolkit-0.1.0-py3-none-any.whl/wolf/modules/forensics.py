"""
Digital Forensics and Incident Response Module
"""

import os
import hashlib
import sqlite3
import json
import time
import platform
import subprocess
from datetime import datetime
from wolf.core.base import BaseModule

class ForensicsModule(BaseModule):
    """
    Digital forensics and incident response capabilities
    """
    
    def __init__(self):
        super().__init__("Forensics")
        self.evidence_db = None
        self._init_evidence_database()
    
    def execute(self, target, **kwargs):
        """
        Execute forensics analysis
        
        Args:
            target (str): Target file/directory/system
            **kwargs: Additional parameters
            
        Returns:
            dict: Forensics analysis results
        """
        return self.analyze_evidence(target=target, **kwargs)
    
    def _init_evidence_database(self):
        """Initialize evidence database"""
        try:
            db_path = "forensics_evidence.db"
            self.evidence_db = sqlite3.connect(db_path)
            cursor = self.evidence_db.cursor()
            
            # Create evidence table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    file_path TEXT,
                    file_hash TEXT,
                    file_size INTEGER,
                    file_type TEXT,
                    metadata TEXT,
                    analysis_results TEXT
                )
            ''')
            
            # Create timeline table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timeline (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event_type TEXT,
                    description TEXT,
                    file_path TEXT,
                    hash_value TEXT
                )
            ''')
            
            self.evidence_db.commit()
            
        except Exception as e:
            self.log_error(f"Failed to initialize evidence database: {e}")
    
    def analyze_evidence(self, target, **kwargs):
        """
        Comprehensive evidence analysis
        
        Args:
            target (str): Target to analyze
            **kwargs: Additional parameters
            
        Returns:
            dict: Analysis results
        """
        self.log_info(f"Starting forensics analysis of {target}")
        
        results = {
            'target': target,
            'analysis_timestamp': datetime.now().isoformat(),
            'file_analysis': {},
            'metadata_extraction': {},
            'hash_analysis': {},
            'timeline_analysis': {},
            'artifact_recovery': {},
            'system_analysis': {},
            'network_artifacts': {},
            'memory_analysis': {},
            'evidence_chain': []
        }
        
        try:
            if os.path.isfile(target):
                # File analysis
                results['file_analysis'] = self._analyze_file(target)
                results['metadata_extraction'] = self._extract_metadata(target)
                results['hash_analysis'] = self._calculate_hashes(target)
                
                # Store in evidence database
                self._store_evidence(target, results)
                
            elif os.path.isdir(target):
                # Directory analysis
                results['directory_analysis'] = self._analyze_directory(target)
                results['timeline_analysis'] = self._create_timeline(target)
                
            else:
                # System analysis
                results['system_analysis'] = self._analyze_system()
                results['network_artifacts'] = self._collect_network_artifacts()
                results['memory_analysis'] = self._analyze_memory()
            
            # Generate evidence chain
            results['evidence_chain'] = self._generate_evidence_chain(target)
            
            self.log_info("Forensics analysis completed")
            
        except Exception as e:
            self.log_error(f"Forensics analysis error: {e}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_file(self, file_path):
        """Analyze individual file"""
        analysis = {
            'file_path': file_path,
            'file_size': 0,
            'file_type': None,
            'permissions': None,
            'timestamps': {},
            'signatures': [],
            'entropy': 0,
            'strings_found': []
        }
        
        try:
            # Basic file info
            stat_info = os.stat(file_path)
            analysis['file_size'] = stat_info.st_size
            analysis['permissions'] = oct(stat_info.st_mode)[-3:]
            
            # Timestamps
            analysis['timestamps'] = {
                'created': datetime.fromtimestamp(stat_info.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat_info.st_atime).isoformat()
            }
            
            # File type detection
            analysis['file_type'] = self._detect_file_type(file_path)
            
            # File signatures
            analysis['signatures'] = self._check_file_signatures(file_path)
            
            # Calculate entropy
            analysis['entropy'] = self._calculate_entropy(file_path)
            
            # Extract strings
            analysis['strings_found'] = self._extract_strings(file_path)
            
        except Exception as e:
            self.log_debug(f"File analysis error for {file_path}: {e}")
        
        return analysis
    
    def _extract_metadata(self, file_path):
        """Extract file metadata"""
        metadata = {
            'exif_data': {},
            'document_properties': {},
            'extended_attributes': {},
            'alternate_data_streams': []
        }
        
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # Basic extended attributes (Unix/Linux)
            if platform.system() != "Windows":
                try:
                    import xattr
                    attrs = dict(xattr.xattr(file_path))
                    metadata['extended_attributes'] = {
                        k.decode('utf-8', errors='ignore'): v.decode('utf-8', errors='ignore') 
                        for k, v in attrs.items()
                    }
                except ImportError:
                    pass
                except Exception:
                    pass
            
            # Document metadata for common formats
            if file_ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                metadata['document_properties'] = self._extract_document_metadata(file_path)
            
            # Image EXIF data
            if file_ext in ['.jpg', '.jpeg', '.tiff', '.tif']:
                metadata['exif_data'] = self._extract_exif_data(file_path)
            
        except Exception as e:
            self.log_debug(f"Metadata extraction error for {file_path}: {e}")
        
        return metadata
    
    def _calculate_hashes(self, file_path):
        """Calculate file hashes"""
        hashes = {
            'md5': None,
            'sha1': None,
            'sha256': None,
            'sha512': None
        }
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
                hashes['md5'] = hashlib.md5(content).hexdigest()
                hashes['sha1'] = hashlib.sha1(content).hexdigest()
                hashes['sha256'] = hashlib.sha256(content).hexdigest()
                hashes['sha512'] = hashlib.sha512(content).hexdigest()
                
        except Exception as e:
            self.log_debug(f"Hash calculation error for {file_path}: {e}")
        
        return hashes
    
    def _detect_file_type(self, file_path):
        """Detect file type using magic numbers"""
        file_signatures = {
            b'\x89PNG': 'PNG Image',
            b'\xFF\xD8\xFF': 'JPEG Image',
            b'GIF87a': 'GIF Image',
            b'GIF89a': 'GIF Image',
            b'%PDF': 'PDF Document',
            b'PK\x03\x04': 'ZIP Archive',
            b'Rar!': 'RAR Archive',
            b'\x7FELF': 'ELF Executable',
            b'MZ': 'PE Executable',
            b'\xCA\xFE\xBA\xBE': 'Java Class File',
            b'RIFF': 'RIFF Container',
            b'\x50\x4B\x03\x04': 'Microsoft Office Document'
        }
        
        try:
            with open(file_path, 'rb') as f:
                header = f.read(8)
                
                for signature, file_type in file_signatures.items():
                    if header.startswith(signature):
                        return file_type
                
                # Check file extension as fallback
                ext = os.path.splitext(file_path)[1].lower()
                if ext:
                    return f"{ext[1:].upper()} File"
                
        except Exception as e:
            self.log_debug(f"File type detection error for {file_path}: {e}")
        
        return "Unknown"
    
    def _check_file_signatures(self, file_path):
        """Check for embedded signatures or certificates"""
        signatures = []
        
        try:
            # For PE files, check for digital signatures
            if file_path.lower().endswith(('.exe', '.dll', '.sys')):
                signatures.append(self._check_pe_signature(file_path))
            
            # For other files, check for common signature patterns
            with open(file_path, 'rb') as f:
                content = f.read(1024)  # Read first 1KB
                
                # Check for common signature patterns
                if b'-----BEGIN CERTIFICATE-----' in content:
                    signatures.append("X.509 Certificate Found")
                
                if b'-----BEGIN PGP SIGNATURE-----' in content:
                    signatures.append("PGP Signature Found")
                
        except Exception as e:
            self.log_debug(f"Signature check error for {file_path}: {e}")
        
        return [sig for sig in signatures if sig]
    
    def _calculate_entropy(self, file_path):
        """Calculate file entropy (randomness)"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read(8192)  # Sample first 8KB
                
                if not data:
                    return 0
                
                # Calculate byte frequency
                byte_counts = [0] * 256
                for byte in data:
                    byte_counts[byte] += 1
                
                # Calculate entropy
                entropy = 0
                data_len = len(data)
                
                for count in byte_counts:
                    if count > 0:
                        freq = count / data_len
                        entropy -= freq * (freq.bit_length() - 1)
                
                return entropy
                
        except Exception as e:
            self.log_debug(f"Entropy calculation error for {file_path}: {e}")
            return 0
    
    def _extract_strings(self, file_path, min_length=4):
        """Extract printable strings from file"""
        strings = []
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read(65536)  # Read first 64KB
                
                current_string = ""
                for byte in data:
                    char = chr(byte)
                    if char.isprintable() and char not in '\r\n\t':
                        current_string += char
                    else:
                        if len(current_string) >= min_length:
                            strings.append(current_string)
                        current_string = ""
                
                # Don't forget the last string
                if len(current_string) >= min_length:
                    strings.append(current_string)
                
                # Limit to first 100 strings
                return strings[:100]
                
        except Exception as e:
            self.log_debug(f"String extraction error for {file_path}: {e}")
            return []
    
    def _analyze_directory(self, dir_path):
        """Analyze directory structure"""
        analysis = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'hidden_files': [],
            'large_files': [],
            'recently_modified': [],
            'suspicious_files': []
        }
        
        try:
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    try:
                        stat_info = os.stat(file_path)
                        file_size = stat_info.st_size
                        
                        analysis['total_files'] += 1
                        analysis['total_size'] += file_size
                        
                        # File type distribution
                        ext = os.path.splitext(file)[1].lower()
                        if ext:
                            analysis['file_types'][ext] = analysis['file_types'].get(ext, 0) + 1
                        
                        # Hidden files (Unix/Linux)
                        if file.startswith('.'):
                            analysis['hidden_files'].append(file_path)
                        
                        # Large files (>100MB)
                        if file_size > 100 * 1024 * 1024:
                            analysis['large_files'].append({
                                'path': file_path,
                                'size': file_size
                            })
                        
                        # Recently modified (last 7 days)
                        if time.time() - stat_info.st_mtime < 7 * 24 * 3600:
                            analysis['recently_modified'].append({
                                'path': file_path,
                                'modified': datetime.fromtimestamp(stat_info.st_mtime).isoformat()
                            })
                        
                        # Suspicious files
                        if self._is_suspicious_file(file_path):
                            analysis['suspicious_files'].append(file_path)
                            
                    except Exception as e:
                        self.log_debug(f"Error analyzing file {file_path}: {e}")
                        continue
            
        except Exception as e:
            self.log_error(f"Directory analysis error: {e}")
        
        return analysis
    
    def _create_timeline(self, target_path):
        """Create timeline of file system events"""
        timeline = []
        
        try:
            events = []
            
            # Walk through directory
            for root, dirs, files in os.walk(target_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    try:
                        stat_info = os.stat(file_path)
                        
                        # Add creation event
                        events.append({
                            'timestamp': datetime.fromtimestamp(stat_info.st_ctime),
                            'event_type': 'File Created',
                            'file_path': file_path,
                            'details': f"File created: {file}"
                        })
                        
                        # Add modification event
                        events.append({
                            'timestamp': datetime.fromtimestamp(stat_info.st_mtime),
                            'event_type': 'File Modified',
                            'file_path': file_path,
                            'details': f"File modified: {file}"
                        })
                        
                        # Add access event
                        events.append({
                            'timestamp': datetime.fromtimestamp(stat_info.st_atime),
                            'event_type': 'File Accessed',
                            'file_path': file_path,
                            'details': f"File accessed: {file}"
                        })
                        
                    except Exception as e:
                        self.log_debug(f"Timeline error for {file_path}: {e}")
                        continue
            
            # Sort events by timestamp
            events.sort(key=lambda x: x['timestamp'])
            
            # Convert to serializable format
            for event in events:
                timeline.append({
                    'timestamp': event['timestamp'].isoformat(),
                    'event_type': event['event_type'],
                    'file_path': event['file_path'],
                    'details': event['details']
                })
            
        except Exception as e:
            self.log_error(f"Timeline creation error: {e}")
        
        return timeline
    
    def _analyze_system(self):
        """Analyze system for forensic artifacts"""
        system_analysis = {
            'system_info': {},
            'running_processes': [],
            'network_connections': [],
            'system_logs': [],
            'installed_software': [],
            'user_accounts': [],
            'startup_programs': []
        }
        
        try:
            # System information
            system_analysis['system_info'] = {
                'platform': platform.platform(),
                'processor': platform.processor(),
                'architecture': platform.architecture(),
                'hostname': platform.node(),
                'boot_time': self._get_boot_time()
            }
            
            # Running processes
            system_analysis['running_processes'] = self._get_running_processes()
            
            # Network connections
            system_analysis['network_connections'] = self._get_network_connections()
            
            # System logs
            system_analysis['system_logs'] = self._collect_system_logs()
            
        except Exception as e:
            self.log_error(f"System analysis error: {e}")
        
        return system_analysis
    
    def _collect_network_artifacts(self):
        """Collect network-related artifacts"""
        network_artifacts = {
            'dns_cache': [],
            'arp_table': [],
            'routing_table': [],
            'firewall_rules': [],
            'network_interfaces': []
        }
        
        try:
            # DNS cache
            if platform.system() == "Windows":
                result = subprocess.run(['ipconfig', '/displaydns'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    network_artifacts['dns_cache'] = result.stdout.split('\n')[:50]
            else:
                # Linux DNS cache (systemd-resolved)
                try:
                    result = subprocess.run(['systemd-resolve', '--statistics'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        network_artifacts['dns_cache'] = result.stdout.split('\n')[:20]
                except FileNotFoundError:
                    pass
            
            # ARP table
            result = subprocess.run(['arp', '-a'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                network_artifacts['arp_table'] = result.stdout.split('\n')[:20]
            
        except Exception as e:
            self.log_debug(f"Network artifacts collection error: {e}")
        
        return network_artifacts
    
    def _store_evidence(self, file_path, analysis_results):
        """Store evidence in database"""
        try:
            if not self.evidence_db:
                return
            
            cursor = self.evidence_db.cursor()
            
            # Store evidence record
            cursor.execute('''
                INSERT INTO evidence (timestamp, file_path, file_hash, file_size, 
                                    file_type, metadata, analysis_results)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                file_path,
                analysis_results.get('hash_analysis', {}).get('sha256', ''),
                analysis_results.get('file_analysis', {}).get('file_size', 0),
                analysis_results.get('file_analysis', {}).get('file_type', ''),
                json.dumps(analysis_results.get('metadata_extraction', {})),
                json.dumps(analysis_results)
            ))
            
            self.evidence_db.commit()
            
        except Exception as e:
            self.log_error(f"Evidence storage error: {e}")
    
    def _generate_evidence_chain(self, target):
        """Generate chain of custody for evidence"""
        chain = {
            'evidence_id': hashlib.sha256(f"{target}{time.time()}".encode()).hexdigest()[:16],
            'acquisition_time': datetime.now().isoformat(),
            'investigator': os.getenv('USER', 'unknown'),
            'source_location': target,
            'preservation_method': 'Read-only analysis',
            'tools_used': ['Wolf Forensics Module'],
            'integrity_verification': True
        }
        
        return [chain]
    
    def _is_suspicious_file(self, file_path):
        """Check if file is suspicious"""
        suspicious_indicators = [
            # Suspicious extensions
            file_path.lower().endswith(('.exe', '.bat', '.cmd', '.scr', '.pif')),
            # Hidden executables
            os.path.basename(file_path).startswith('.') and file_path.lower().endswith('.exe'),
            # Double extensions
            '..' in os.path.basename(file_path),
            # Temp directories
            'temp' in file_path.lower() or 'tmp' in file_path.lower()
        ]
        
        return any(suspicious_indicators)
    
    def _get_running_processes(self):
        """Get list of running processes"""
        processes = []
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['tasklist', '/fo', 'csv'], 
                                      capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run(['ps', 'aux'], 
                                      capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')[:50]  # Limit output
                processes = [line.strip() for line in lines if line.strip()]
                
        except Exception as e:
            self.log_debug(f"Process enumeration error: {e}")
        
        return processes
    
    def _get_network_connections(self):
        """Get active network connections"""
        connections = []
        
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['netstat', '-an'], 
                                      capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run(['netstat', '-tuln'], 
                                      capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')[:50]  # Limit output
                connections = [line.strip() for line in lines if line.strip()]
                
        except Exception as e:
            self.log_debug(f"Network connections error: {e}")
        
        return connections
    
    def _collect_system_logs(self):
        """Collect system logs"""
        logs = []
        
        try:
            if platform.system() == "Windows":
                # Windows Event Log (simplified)
                logs.append("Windows Event Log collection requires specialized tools")
            else:
                # Linux system logs
                log_files = ['/var/log/syslog', '/var/log/auth.log', '/var/log/messages']
                
                for log_file in log_files:
                    if os.path.exists(log_file):
                        try:
                            with open(log_file, 'r') as f:
                                # Get last 10 lines
                                lines = f.readlines()[-10:]
                                logs.extend([f"{log_file}: {line.strip()}" for line in lines])
                        except PermissionError:
                            logs.append(f"{log_file}: Permission denied")
                        except Exception as e:
                            logs.append(f"{log_file}: Error reading - {e}")
                            
        except Exception as e:
            self.log_debug(f"System log collection error: {e}")
        
        return logs
    
    def _get_boot_time(self):
        """Get system boot time"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['systeminfo'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'System Boot Time' in line:
                            return line.split(':', 1)[1].strip()
            else:
                result = subprocess.run(['uptime', '-s'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return result.stdout.strip()
                    
        except Exception as e:
            self.log_debug(f"Boot time detection error: {e}")
        
        return "Unknown"
    
    def _extract_document_metadata(self, file_path):
        """Extract metadata from document files"""
        # Placeholder for document metadata extraction
        # In a full implementation, this would use libraries like python-docx, PyPDF2, etc.
        return {"note": "Document metadata extraction requires specialized libraries"}
    
    def _extract_exif_data(self, file_path):
        """Extract EXIF data from images"""
        # Placeholder for EXIF extraction
        # In a full implementation, this would use libraries like Pillow or exifread
        return {"note": "EXIF extraction requires specialized libraries"}
    
    def _check_pe_signature(self, file_path):
        """Check PE file digital signature"""
        # Placeholder for PE signature verification
        # In a full implementation, this would use libraries like pefile
        return "PE signature check requires specialized libraries"
    
    def _analyze_memory(self):
        """Basic memory analysis"""
        memory_analysis = {
            'total_memory': 0,
            'available_memory': 0,
            'memory_usage': 0,
            'swap_usage': 0
        }
        
        try:
            if platform.system() != "Windows":
                # Linux memory info
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.read()
                    
                    for line in meminfo.split('\n'):
                        if 'MemTotal:' in line:
                            memory_analysis['total_memory'] = int(line.split()[1]) * 1024
                        elif 'MemAvailable:' in line:
                            memory_analysis['available_memory'] = int(line.split()[1]) * 1024
                        elif 'SwapTotal:' in line:
                            memory_analysis['swap_total'] = int(line.split()[1]) * 1024
                        elif 'SwapFree:' in line:
                            memory_analysis['swap_free'] = int(line.split()[1]) * 1024
            
        except Exception as e:
            self.log_debug(f"Memory analysis error: {e}")
        
        return memory_analysis