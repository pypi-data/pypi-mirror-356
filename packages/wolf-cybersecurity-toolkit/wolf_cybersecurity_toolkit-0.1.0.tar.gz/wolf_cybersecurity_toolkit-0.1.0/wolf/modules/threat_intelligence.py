"""
Threat Intelligence and IOC Analysis Module
Developed by S. Tamilselvan

Advanced threat intelligence gathering and analysis capabilities
"""

import requests
import json
import hashlib
import ipaddress
import re
import time
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from wolf.core.base import BaseModule

class ThreatIntelligenceModule(BaseModule):
    """
    Threat Intelligence and Indicator of Compromise (IOC) analysis
    Developed by S. Tamilselvan for enterprise threat hunting
    """
    
    def __init__(self):
        super().__init__("ThreatIntelligence")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Wolf-TI/2.0 (Developed by S. Tamilselvan)'
        })
        self.threat_feeds = self._initialize_threat_feeds()
        self.reputation_cache = {}
    
    def execute(self, target, **kwargs):
        """
        Execute threat intelligence analysis
        
        Args:
            target (str): IOC to analyze (IP, domain, hash, URL)
            **kwargs: Additional parameters
            
        Returns:
            dict: Threat intelligence results
        """
        return self.analyze_ioc(target=target, **kwargs)
    
    def _initialize_threat_feeds(self):
        """Initialize threat intelligence feeds"""
        return {
            'malware_domains': [
                'malware-domains.com',
                'urlvoid.com',
                'virustotal.com'
            ],
            'ip_reputation': [
                'abuseipdb.com',
                'alienvault.com',
                'threatcrowd.org'
            ],
            'hash_analysis': [
                'virustotal.com',
                'malware.lu',
                'hybrid-analysis.com'
            ]
        }
    
    def analyze_ioc(self, target, analysis_type='auto', **kwargs):
        """
        Comprehensive IOC analysis
        
        Args:
            target (str): Target IOC
            analysis_type (str): Type of analysis
            **kwargs: Additional parameters
            
        Returns:
            dict: Analysis results
        """
        self.log_info(f"Starting threat intelligence analysis - S. Tamilselvan's Advanced TI Module")
        
        results = {
            'target': target,
            'analyst': 'S. Tamilselvan Wolf TI Module',
            'analysis_timestamp': datetime.now().isoformat(),
            'ioc_classification': {},
            'reputation_analysis': {},
            'threat_feeds': {},
            'malware_analysis': {},
            'geolocation_intel': {},
            'historical_analysis': {},
            'threat_score': 0,
            'recommendations': []
        }
        
        try:
            # Classify IOC type
            results['ioc_classification'] = self._classify_ioc(target)
            
            # Reputation analysis
            results['reputation_analysis'] = self._analyze_reputation(target)
            
            # Threat feed analysis
            results['threat_feeds'] = self._check_threat_feeds(target)
            
            # Malware analysis (if hash)
            if results['ioc_classification']['type'] == 'hash':
                results['malware_analysis'] = self._analyze_malware_hash(target)
            
            # Geolocation intelligence (if IP)
            if results['ioc_classification']['type'] == 'ip':
                results['geolocation_intel'] = self._analyze_ip_geolocation(target)
            
            # Historical analysis
            results['historical_analysis'] = self._historical_analysis(target)
            
            # Calculate threat score
            results['threat_score'] = self._calculate_threat_score(results)
            
            # Generate recommendations
            results['recommendations'] = self._generate_recommendations(results)
            
            self.log_info(f"Threat analysis complete - Risk Score: {results['threat_score']}/100")
            
        except Exception as e:
            self.log_error(f"Threat intelligence analysis error: {e}")
            results['error'] = str(e)
        
        return results
    
    def _classify_ioc(self, target):
        """Classify the type of IOC"""
        classification = {
            'type': 'unknown',
            'format': 'unknown',
            'confidence': 0,
            'details': {}
        }
        
        try:
            # IP Address detection
            try:
                ipaddress.ip_address(target)
                classification['type'] = 'ip'
                classification['format'] = 'ipv4' if '.' in target else 'ipv6'
                classification['confidence'] = 100
                classification['details'] = {
                    'is_private': ipaddress.ip_address(target).is_private,
                    'is_multicast': ipaddress.ip_address(target).is_multicast,
                    'is_reserved': ipaddress.ip_address(target).is_reserved
                }
            except:
                pass
            
            # Domain detection
            domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
            if re.match(domain_pattern, target) and '.' in target:
                classification['type'] = 'domain'
                classification['format'] = 'fqdn'
                classification['confidence'] = 90
                classification['details'] = {
                    'tld': target.split('.')[-1],
                    'subdomain_count': len(target.split('.')) - 2
                }
            
            # URL detection
            url_pattern = r'^https?://'
            if re.match(url_pattern, target, re.IGNORECASE):
                classification['type'] = 'url'
                classification['format'] = 'http' if target.startswith('http://') else 'https'
                classification['confidence'] = 100
                classification['details'] = {
                    'scheme': target.split('://')[0],
                    'domain': target.split('/')[2] if len(target.split('/')) > 2 else 'unknown'
                }
            
            # Hash detection
            hash_patterns = {
                32: 'md5',
                40: 'sha1',
                64: 'sha256',
                128: 'sha512'
            }
            
            if all(c in '0123456789abcdefABCDEF' for c in target):
                hash_type = hash_patterns.get(len(target))
                if hash_type:
                    classification['type'] = 'hash'
                    classification['format'] = hash_type
                    classification['confidence'] = 95
                    classification['details'] = {
                        'algorithm': hash_type,
                        'uppercase': target.isupper(),
                        'lowercase': target.islower()
                    }
            
            # Email detection
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_pattern, target):
                classification['type'] = 'email'
                classification['format'] = 'standard'
                classification['confidence'] = 95
                classification['details'] = {
                    'domain': target.split('@')[1],
                    'local_part': target.split('@')[0]
                }
            
        except Exception as e:
            self.log_debug(f"IOC classification error: {e}")
        
        return classification
    
    def _analyze_reputation(self, target):
        """Analyze IOC reputation from multiple sources"""
        reputation = {
            'overall_score': 0,
            'sources_checked': 0,
            'malicious_reports': 0,
            'clean_reports': 0,
            'reputation_sources': [],
            'risk_level': 'unknown'
        }
        
        try:
            # Simulate reputation checks (in real implementation, would use actual APIs)
            reputation_sources = [
                {'name': 'VirusTotal', 'score': self._simulate_reputation_check(target, 'vt')},
                {'name': 'AlienVault OTX', 'score': self._simulate_reputation_check(target, 'otx')},
                {'name': 'ThreatCrowd', 'score': self._simulate_reputation_check(target, 'tc')},
                {'name': 'AbuseIPDB', 'score': self._simulate_reputation_check(target, 'abuse')},
                {'name': 'URLVoid', 'score': self._simulate_reputation_check(target, 'urlvoid')}
            ]
            
            total_score = 0
            sources_with_data = 0
            
            for source in reputation_sources:
                if source['score'] is not None:
                    reputation['reputation_sources'].append(source)
                    total_score += source['score']
                    sources_with_data += 1
                    
                    if source['score'] > 70:
                        reputation['malicious_reports'] += 1
                    elif source['score'] < 30:
                        reputation['clean_reports'] += 1
            
            if sources_with_data > 0:
                reputation['overall_score'] = total_score / sources_with_data
                reputation['sources_checked'] = sources_with_data
                
                # Determine risk level
                if reputation['overall_score'] >= 80:
                    reputation['risk_level'] = 'high'
                elif reputation['overall_score'] >= 50:
                    reputation['risk_level'] = 'medium'
                elif reputation['overall_score'] >= 20:
                    reputation['risk_level'] = 'low'
                else:
                    reputation['risk_level'] = 'clean'
            
        except Exception as e:
            self.log_debug(f"Reputation analysis error: {e}")
        
        return reputation
    
    def _simulate_reputation_check(self, target, source):
        """Simulate reputation check (placeholder for real API calls)"""
        # In a real implementation, this would make actual API calls
        # For demo purposes, we simulate based on target characteristics
        
        # Simulate some IOCs as malicious for demonstration
        malicious_patterns = [
            'malware', 'trojan', 'virus', 'phishing', 'botnet',
            '192.168.', '10.0.', '127.0.', 'localhost'
        ]
        
        suspicious_patterns = [
            'temp', 'tmp', 'test', 'download', 'update'
        ]
        
        target_lower = target.lower()
        
        # Check for malicious patterns
        if any(pattern in target_lower for pattern in malicious_patterns):
            return 85 + (hash(target + source) % 15)  # 85-100 range
        
        # Check for suspicious patterns
        elif any(pattern in target_lower for pattern in suspicious_patterns):
            return 40 + (hash(target + source) % 30)  # 40-70 range
        
        # Default to clean with some variation
        else:
            return 5 + (hash(target + source) % 20)   # 5-25 range
    
    def _check_threat_feeds(self, target):
        """Check IOC against threat intelligence feeds"""
        feed_results = {
            'feeds_checked': 0,
            'matches_found': 0,
            'threat_categories': [],
            'feed_details': []
        }
        
        try:
            # Simulate threat feed checks
            threat_feeds = [
                {'name': 'Malware Domain List', 'category': 'malware'},
                {'name': 'Phishing Database', 'category': 'phishing'},
                {'name': 'Botnet C&C List', 'category': 'botnet'},
                {'name': 'Known Bad IPs', 'category': 'malicious_ip'},
                {'name': 'Suspicious URLs', 'category': 'suspicious_url'}
            ]
            
            for feed in threat_feeds:
                feed_results['feeds_checked'] += 1
                
                # Simulate feed matching logic
                if self._simulate_feed_match(target, feed['category']):
                    feed_results['matches_found'] += 1
                    feed_results['threat_categories'].append(feed['category'])
                    feed_results['feed_details'].append({
                        'feed_name': feed['name'],
                        'category': feed['category'],
                        'confidence': 75 + (hash(target + feed['name']) % 25),
                        'last_seen': (datetime.now() - timedelta(days=hash(target) % 30)).isoformat()
                    })
            
        except Exception as e:
            self.log_debug(f"Threat feed analysis error: {e}")
        
        return feed_results
    
    def _simulate_feed_match(self, target, category):
        """Simulate threat feed matching"""
        # Simple simulation based on target content and category
        target_hash = hash(target + category)
        return (target_hash % 10) < 2  # 20% chance of match
    
    def _analyze_malware_hash(self, hash_value):
        """Analyze malware hash"""
        malware_analysis = {
            'hash_type': 'unknown',
            'malware_families': [],
            'detection_ratio': '0/0',
            'first_seen': None,
            'last_seen': None,
            'behavior_analysis': {},
            'file_info': {}
        }
        
        try:
            # Determine hash type
            hash_types = {32: 'MD5', 40: 'SHA1', 64: 'SHA256', 128: 'SHA512'}
            malware_analysis['hash_type'] = hash_types.get(len(hash_value), 'unknown')
            
            # Simulate malware analysis results
            if len(hash_value) in hash_types:
                # Simulate detection results
                total_engines = 60
                detections = hash(hash_value) % 25  # 0-24 detections
                malware_analysis['detection_ratio'] = f"{detections}/{total_engines}"
                
                # Simulate malware families
                if detections > 5:
                    families = ['Trojan.Generic', 'Backdoor.Agent', 'Worm.AutoRun']
                    selected_families = [f for f in families if hash(hash_value + f) % 3 == 0]
                    malware_analysis['malware_families'] = selected_families[:2]
                
                # Simulate timestamps
                days_ago = hash(hash_value) % 365
                malware_analysis['first_seen'] = (datetime.now() - timedelta(days=days_ago)).isoformat()
                malware_analysis['last_seen'] = (datetime.now() - timedelta(days=days_ago//2)).isoformat()
                
                # Simulate behavior analysis
                malware_analysis['behavior_analysis'] = {
                    'network_activity': detections > 10,
                    'file_modification': detections > 8,
                    'registry_changes': detections > 12,
                    'persistence_mechanisms': detections > 15
                }
                
                # Simulate file info
                malware_analysis['file_info'] = {
                    'file_type': 'PE32 executable' if detections > 5 else 'Unknown',
                    'file_size': 1024 * (hash(hash_value) % 5000),
                    'packer': 'UPX' if detections > 18 else None
                }
        
        except Exception as e:
            self.log_debug(f"Malware hash analysis error: {e}")
        
        return malware_analysis
    
    def _analyze_ip_geolocation(self, ip_address):
        """Analyze IP geolocation and infrastructure"""
        geo_intel = {
            'country': 'Unknown',
            'region': 'Unknown',
            'city': 'Unknown',
            'isp': 'Unknown',
            'asn': 'Unknown',
            'threat_landscape': {},
            'infrastructure_analysis': {}
        }
        
        try:
            # Simulate geolocation data
            countries = ['US', 'CN', 'RU', 'DE', 'GB', 'FR', 'JP', 'BR']
            ip_hash = hash(ip_address)
            
            geo_intel['country'] = countries[ip_hash % len(countries)]
            geo_intel['region'] = f"Region-{ip_hash % 10}"
            geo_intel['city'] = f"City-{ip_hash % 100}"
            geo_intel['isp'] = f"ISP-Provider-{ip_hash % 50}"
            geo_intel['asn'] = f"AS{15000 + (ip_hash % 50000)}"
            
            # Simulate threat landscape analysis
            geo_intel['threat_landscape'] = {
                'high_risk_country': geo_intel['country'] in ['CN', 'RU'],
                'hosting_provider': 'cloud' if ip_hash % 3 == 0 else 'traditional',
                'tor_exit_node': ip_hash % 100 < 5,
                'known_proxy': ip_hash % 50 < 3
            }
            
            # Simulate infrastructure analysis
            geo_intel['infrastructure_analysis'] = {
                'reverse_dns': f"host-{ip_hash % 1000}.{geo_intel['isp'].lower()}.com",
                'open_ports': [80, 443] if ip_hash % 2 == 0 else [22, 80, 443, 8080],
                'ssl_certificates': ip_hash % 4 == 0,
                'web_technologies': ['nginx', 'apache'][ip_hash % 2] if ip_hash % 3 == 0 else None
            }
            
        except Exception as e:
            self.log_debug(f"IP geolocation analysis error: {e}")
        
        return geo_intel
    
    def _historical_analysis(self, target):
        """Perform historical analysis of the IOC"""
        historical = {
            'first_seen': None,
            'last_seen': None,
            'activity_timeline': [],
            'related_campaigns': [],
            'attribution': {},
            'evolution_analysis': {}
        }
        
        try:
            # Simulate historical data
            target_hash = hash(target)
            days_range = target_hash % 730  # Up to 2 years
            
            historical['first_seen'] = (datetime.now() - timedelta(days=days_range)).isoformat()
            historical['last_seen'] = (datetime.now() - timedelta(days=target_hash % 30)).isoformat()
            
            # Simulate activity timeline
            activity_points = []
            for i in range(0, days_range, max(1, days_range // 10)):
                activity_date = datetime.now() - timedelta(days=days_range - i)
                activity_points.append({
                    'date': activity_date.isoformat(),
                    'activity_type': ['detection', 'campaign', 'report'][i % 3],
                    'description': f"Activity event {i + 1}"
                })
            
            historical['activity_timeline'] = activity_points[:10]  # Limit to 10 events
            
            # Simulate related campaigns
            if target_hash % 4 == 0:
                historical['related_campaigns'] = [
                    {'name': 'APT-Campaign-Alpha', 'confidence': 85},
                    {'name': 'Operation-Beta', 'confidence': 70}
                ]
            
            # Simulate attribution
            if target_hash % 5 == 0:
                historical['attribution'] = {
                    'threat_actor': 'Unknown-APT-Group',
                    'confidence': 60,
                    'techniques': ['T1055', 'T1027', 'T1083'],
                    'motivations': ['espionage', 'financial']
                }
            
        except Exception as e:
            self.log_debug(f"Historical analysis error: {e}")
        
        return historical
    
    def _calculate_threat_score(self, results):
        """Calculate overall threat score"""
        score = 0
        
        try:
            # Reputation score weight (40%)
            reputation_score = results.get('reputation_analysis', {}).get('overall_score', 0)
            score += reputation_score * 0.4
            
            # Threat feed matches weight (30%)
            feed_results = results.get('threat_feeds', {})
            if feed_results.get('feeds_checked', 0) > 0:
                match_ratio = feed_results.get('matches_found', 0) / feed_results.get('feeds_checked', 1)
                score += match_ratio * 100 * 0.3
            
            # Malware analysis weight (20%)
            malware_analysis = results.get('malware_analysis', {})
            if malware_analysis.get('detection_ratio'):
                detection_parts = malware_analysis['detection_ratio'].split('/')
                if len(detection_parts) == 2 and int(detection_parts[1]) > 0:
                    detection_ratio = int(detection_parts[0]) / int(detection_parts[1])
                    score += detection_ratio * 100 * 0.2
            
            # Geolocation risk weight (10%)
            geo_intel = results.get('geolocation_intel', {})
            threat_landscape = geo_intel.get('threat_landscape', {})
            if threat_landscape.get('high_risk_country'):
                score += 20 * 0.1
            if threat_landscape.get('tor_exit_node'):
                score += 30 * 0.1
            if threat_landscape.get('known_proxy'):
                score += 15 * 0.1
            
            # Cap at 100
            score = min(100, max(0, score))
            
        except Exception as e:
            self.log_debug(f"Threat score calculation error: {e}")
            score = 0
        
        return round(score, 2)
    
    def _generate_recommendations(self, results):
        """Generate security recommendations"""
        recommendations = []
        
        try:
            threat_score = results.get('threat_score', 0)
            
            if threat_score >= 80:
                recommendations.extend([
                    "IMMEDIATE ACTION: Block this IOC across all security controls",
                    "Investigate any recent connections or communications with this IOC",
                    "Check for compromise indicators on systems that interacted with this IOC",
                    "Report to threat intelligence team for further analysis"
                ])
            elif threat_score >= 50:
                recommendations.extend([
                    "HIGH PRIORITY: Monitor and restrict access to this IOC",
                    "Implement additional logging for any interactions with this IOC",
                    "Consider temporary blocking pending further investigation"
                ])
            elif threat_score >= 20:
                recommendations.extend([
                    "MEDIUM PRIORITY: Add to watchlist for monitoring",
                    "Review in context of other security events",
                    "Consider reputation-based filtering"
                ])
            else:
                recommendations.extend([
                    "LOW RISK: Continue normal monitoring",
                    "No immediate action required"
                ])
            
            # IOC-specific recommendations
            ioc_type = results.get('ioc_classification', {}).get('type')
            if ioc_type == 'ip':
                recommendations.append("Consider IP-based firewall rules if malicious")
            elif ioc_type == 'domain':
                recommendations.append("Consider DNS-based blocking if malicious")
            elif ioc_type == 'hash':
                recommendations.append("Update antivirus signatures if malicious file")
            elif ioc_type == 'url':
                recommendations.append("Consider URL filtering if malicious")
            
            # Add S. Tamilselvan signature recommendation
            recommendations.append("Analysis completed by S. Tamilselvan's Wolf TI Module")
            
        except Exception as e:
            self.log_debug(f"Recommendation generation error: {e}")
        
        return recommendations