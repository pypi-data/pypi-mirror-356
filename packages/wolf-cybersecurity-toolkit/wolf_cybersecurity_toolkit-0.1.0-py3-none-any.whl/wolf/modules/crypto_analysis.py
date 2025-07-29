"""
Cryptographic Analysis and Hash Cracking Module
"""

import hashlib
import hmac
import base64
import binascii
import itertools
import string
import time
from concurrent.futures import ThreadPoolExecutor
from wolf.core.base import BaseModule

class CryptoAnalysisModule(BaseModule):
    """
    Cryptographic analysis, hash identification, and password cracking capabilities
    """
    
    def __init__(self):
        super().__init__("CryptoAnalysis")
        self.common_passwords = self._load_common_passwords()
        self.hash_algorithms = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha224': hashlib.sha224,
            'sha256': hashlib.sha256,
            'sha384': hashlib.sha384,
            'sha512': hashlib.sha512
        }
    
    def execute(self, target, **kwargs):
        """
        Execute cryptographic analysis
        
        Args:
            target (str): Hash or encrypted data to analyze
            **kwargs: Additional parameters
            
        Returns:
            dict: Analysis results
        """
        return self.analyze_crypto(target=target, **kwargs)
    
    def analyze_crypto(self, target, analysis_type='auto', **kwargs):
        """
        Comprehensive cryptographic analysis
        
        Args:
            target (str): Target hash or data
            analysis_type (str): Type of analysis (auto, hash, base64, etc.)
            **kwargs: Additional parameters
            
        Returns:
            dict: Analysis results
        """
        self.log_info(f"Starting cryptographic analysis of target")
        
        results = {
            'target': target,
            'analysis_type': analysis_type,
            'hash_identification': {},
            'encoding_detection': {},
            'crack_attempts': {},
            'entropy_analysis': {},
            'pattern_analysis': {},
            'cipher_analysis': {},
            'weakness_assessment': {}
        }
        
        try:
            # Hash identification
            results['hash_identification'] = self._identify_hash(target)
            
            # Encoding detection
            results['encoding_detection'] = self._detect_encoding(target)
            
            # Entropy analysis
            results['entropy_analysis'] = self._analyze_entropy(target)
            
            # Pattern analysis
            results['pattern_analysis'] = self._analyze_patterns(target)
            
            # Cipher analysis
            results['cipher_analysis'] = self._analyze_cipher(target)
            
            # Hash cracking attempts
            if results['hash_identification']['likely_algorithms']:
                results['crack_attempts'] = self._attempt_crack(target, **kwargs)
            
            # Weakness assessment
            results['weakness_assessment'] = self._assess_weaknesses(results)
            
            self.log_info("Cryptographic analysis completed")
            
        except Exception as e:
            self.log_error(f"Cryptographic analysis error: {e}")
            results['error'] = str(e)
        
        return results
    
    def _identify_hash(self, hash_string):
        """Identify hash algorithm based on characteristics"""
        identification = {
            'likely_algorithms': [],
            'length_analysis': {},
            'character_analysis': {},
            'format_analysis': {}
        }
        
        try:
            # Clean the hash string
            cleaned_hash = hash_string.strip()
            
            # Length-based identification
            length = len(cleaned_hash)
            identification['length_analysis']['length'] = length
            
            # Character set analysis
            chars = set(cleaned_hash.lower())
            is_hex = all(c in '0123456789abcdef' for c in chars)
            is_base64 = all(c in string.ascii_letters + string.digits + '+/=' for c in cleaned_hash)
            
            identification['character_analysis'] = {
                'is_hexadecimal': is_hex,
                'is_base64_chars': is_base64,
                'character_set': ''.join(sorted(chars))
            }
            
            # Algorithm identification by length and format
            if is_hex:
                if length == 32:
                    identification['likely_algorithms'].append('MD5')
                elif length == 40:
                    identification['likely_algorithms'].append('SHA1')
                elif length == 56:
                    identification['likely_algorithms'].append('SHA224')
                elif length == 64:
                    identification['likely_algorithms'].append('SHA256')
                elif length == 96:
                    identification['likely_algorithms'].append('SHA384')
                elif length == 128:
                    identification['likely_algorithms'].append('SHA512')
                elif length == 16:
                    identification['likely_algorithms'].append('MD5 (truncated)')
                elif length == 8:
                    identification['likely_algorithms'].append('CRC32')
            
            # Check for common hash formats
            if '$' in cleaned_hash:
                parts = cleaned_hash.split('$')
                if len(parts) >= 3:
                    hash_type = parts[1]
                    if hash_type == '1':
                        identification['likely_algorithms'].append('MD5 Crypt')
                    elif hash_type == '5':
                        identification['likely_algorithms'].append('SHA256 Crypt')
                    elif hash_type == '6':
                        identification['likely_algorithms'].append('SHA512 Crypt')
                    elif hash_type == '2a' or hash_type == '2b':
                        identification['likely_algorithms'].append('Bcrypt')
            
            # Base64 encoded hashes
            if is_base64 and length % 4 == 0:
                try:
                    decoded = base64.b64decode(cleaned_hash)
                    decoded_length = len(decoded)
                    if decoded_length == 16:
                        identification['likely_algorithms'].append('MD5 (Base64)')
                    elif decoded_length == 20:
                        identification['likely_algorithms'].append('SHA1 (Base64)')
                    elif decoded_length == 32:
                        identification['likely_algorithms'].append('SHA256 (Base64)')
                except:
                    pass
            
            # NTLM hash (often 32 hex chars, uppercase)
            if length == 32 and is_hex and cleaned_hash.isupper():
                identification['likely_algorithms'].append('NTLM')
            
        except Exception as e:
            self.log_debug(f"Hash identification error: {e}")
        
        return identification
    
    def _detect_encoding(self, data):
        """Detect encoding schemes"""
        encoding_results = {
            'base64_valid': False,
            'hex_valid': False,
            'url_encoded': False,
            'decoded_attempts': {}
        }
        
        try:
            # Base64 detection and decoding
            try:
                if len(data) % 4 == 0:
                    decoded = base64.b64decode(data)
                    encoding_results['base64_valid'] = True
                    encoding_results['decoded_attempts']['base64'] = {
                        'success': True,
                        'decoded_length': len(decoded),
                        'printable': all(32 <= b <= 126 for b in decoded[:50])
                    }
            except:
                encoding_results['decoded_attempts']['base64'] = {'success': False}
            
            # Hex decoding
            try:
                if all(c in '0123456789abcdefABCDEF' for c in data):
                    decoded = bytes.fromhex(data)
                    encoding_results['hex_valid'] = True
                    encoding_results['decoded_attempts']['hex'] = {
                        'success': True,
                        'decoded_length': len(decoded),
                        'printable': all(32 <= b <= 126 for b in decoded[:50])
                    }
            except:
                encoding_results['decoded_attempts']['hex'] = {'success': False}
            
            # URL encoding detection
            if '%' in data:
                import urllib.parse
                try:
                    decoded = urllib.parse.unquote(data)
                    if decoded != data:
                        encoding_results['url_encoded'] = True
                        encoding_results['decoded_attempts']['url'] = {
                            'success': True,
                            'decoded': decoded[:100]
                        }
                except:
                    encoding_results['decoded_attempts']['url'] = {'success': False}
            
        except Exception as e:
            self.log_debug(f"Encoding detection error: {e}")
        
        return encoding_results
    
    def _analyze_entropy(self, data):
        """Analyze entropy of the data"""
        entropy_analysis = {
            'shannon_entropy': 0,
            'min_entropy': 0,
            'character_frequency': {},
            'randomness_assessment': 'unknown'
        }
        
        try:
            # Calculate Shannon entropy
            char_counts = {}
            for char in data:
                char_counts[char] = char_counts.get(char, 0) + 1
            
            data_len = len(data)
            entropy = 0
            
            for count in char_counts.values():
                probability = count / data_len
                if probability > 0:
                    entropy -= probability * (probability.bit_length() - 1)
            
            entropy_analysis['shannon_entropy'] = entropy
            
            # Character frequency analysis
            entropy_analysis['character_frequency'] = {
                char: count / data_len 
                for char, count in sorted(char_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            }
            
            # Randomness assessment
            if entropy > 7.5:
                entropy_analysis['randomness_assessment'] = 'high'
            elif entropy > 6.0:
                entropy_analysis['randomness_assessment'] = 'medium'
            elif entropy > 4.0:
                entropy_analysis['randomness_assessment'] = 'low'
            else:
                entropy_analysis['randomness_assessment'] = 'very_low'
            
        except Exception as e:
            self.log_debug(f"Entropy analysis error: {e}")
        
        return entropy_analysis
    
    def _analyze_patterns(self, data):
        """Analyze patterns in the data"""
        pattern_analysis = {
            'repeated_sequences': [],
            'character_patterns': {},
            'structure_analysis': {}
        }
        
        try:
            # Find repeated sequences
            for length in [2, 3, 4]:
                sequences = {}
                for i in range(len(data) - length + 1):
                    seq = data[i:i+length]
                    sequences[seq] = sequences.get(seq, 0) + 1
                
                repeated = [(seq, count) for seq, count in sequences.items() if count > 1]
                if repeated:
                    pattern_analysis['repeated_sequences'].extend(repeated[:5])
            
            # Character type analysis
            pattern_analysis['character_patterns'] = {
                'digits': sum(1 for c in data if c.isdigit()),
                'uppercase': sum(1 for c in data if c.isupper()),
                'lowercase': sum(1 for c in data if c.islower()),
                'special_chars': sum(1 for c in data if not c.isalnum()),
                'total_length': len(data)
            }
            
            # Structure analysis
            pattern_analysis['structure_analysis'] = {
                'has_separators': any(sep in data for sep in ['-', ':', '$', '.']),
                'all_same_case': data.islower() or data.isupper(),
                'alternating_pattern': self._check_alternating_pattern(data),
                'sequential_chars': self._check_sequential_chars(data)
            }
            
        except Exception as e:
            self.log_debug(f"Pattern analysis error: {e}")
        
        return pattern_analysis
    
    def _analyze_cipher(self, data):
        """Analyze potential cipher types"""
        cipher_analysis = {
            'potential_ciphers': [],
            'caesar_analysis': {},
            'substitution_analysis': {},
            'frequency_analysis': {}
        }
        
        try:
            # Caesar cipher analysis
            if data.isalpha():
                cipher_analysis['caesar_analysis'] = self._analyze_caesar(data)
                if cipher_analysis['caesar_analysis']['likely_shifts']:
                    cipher_analysis['potential_ciphers'].append('Caesar Cipher')
            
            # Simple substitution cipher indicators
            if len(set(data.lower())) == len(string.ascii_lowercase):
                cipher_analysis['potential_ciphers'].append('Simple Substitution')
            
            # ROT13 check
            rot13 = data.encode('ascii', errors='ignore').decode('ascii').translate(
                str.maketrans(
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
                    'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijkl'
                )
            )
            if self._looks_like_text(rot13):
                cipher_analysis['potential_ciphers'].append('ROT13')
                cipher_analysis['rot13_result'] = rot13
            
            # Frequency analysis for alphabetic data
            if data.isalpha():
                cipher_analysis['frequency_analysis'] = self._frequency_analysis(data)
            
        except Exception as e:
            self.log_debug(f"Cipher analysis error: {e}")
        
        return cipher_analysis
    
    def _attempt_crack(self, target_hash, method='dictionary', **kwargs):
        """Attempt to crack the hash"""
        crack_results = {
            'method': method,
            'algorithms_tested': [],
            'found_matches': [],
            'attempts_made': 0,
            'time_taken': 0
        }
        
        start_time = time.time()
        
        try:
            # Get likely algorithms
            hash_id = self._identify_hash(target_hash)
            algorithms = hash_id['likely_algorithms']
            
            if not algorithms:
                # Default to common algorithms
                algorithms = ['MD5', 'SHA1', 'SHA256']
            
            # Dictionary attack
            if method in ['dictionary', 'auto']:
                crack_results.update(self._dictionary_attack(target_hash, algorithms, **kwargs))
            
            # Brute force attack (limited)
            if method in ['brute_force', 'auto'] and not crack_results['found_matches']:
                crack_results.update(self._brute_force_attack(target_hash, algorithms, **kwargs))
            
            crack_results['time_taken'] = time.time() - start_time
            
        except Exception as e:
            self.log_error(f"Hash cracking error: {e}")
        
        return crack_results
    
    def _dictionary_attack(self, target_hash, algorithms, **kwargs):
        """Perform dictionary attack"""
        results = {
            'method': 'dictionary',
            'passwords_tested': 0,
            'found_matches': [],
            'algorithms_tested': []
        }
        
        try:
            # Clean target hash
            target_cleaned = target_hash.strip().lower()
            
            # Test against common passwords
            for password in self.common_passwords[:1000]:  # Limit for performance
                results['passwords_tested'] += 1
                
                for algo_name in algorithms[:3]:  # Limit algorithms
                    if algo_name.upper() in ['MD5', 'SHA1', 'SHA256', 'SHA512']:
                        algo = self.hash_algorithms.get(algo_name.lower())
                        if algo:
                            if algo_name not in results['algorithms_tested']:
                                results['algorithms_tested'].append(algo_name)
                            
                            computed_hash = algo(password.encode()).hexdigest().lower()
                            
                            if computed_hash == target_cleaned:
                                results['found_matches'].append({
                                    'password': password,
                                    'algorithm': algo_name,
                                    'hash': computed_hash
                                })
                                self.log_info(f"Hash cracked: {password} ({algo_name})")
                                return results
            
        except Exception as e:
            self.log_debug(f"Dictionary attack error: {e}")
        
        return results
    
    def _brute_force_attack(self, target_hash, algorithms, **kwargs):
        """Limited brute force attack"""
        results = {
            'method': 'brute_force',
            'passwords_tested': 0,
            'found_matches': [],
            'algorithms_tested': []
        }
        
        try:
            # Very limited brute force (4 chars max, numbers only for safety)
            target_cleaned = target_hash.strip().lower()
            max_length = kwargs.get('max_length', 4)
            charset = kwargs.get('charset', '0123456789')
            
            if max_length > 6:  # Safety limit
                max_length = 6
            
            for length in range(1, max_length + 1):
                for candidate in itertools.product(charset, repeat=length):
                    password = ''.join(candidate)
                    results['passwords_tested'] += 1
                    
                    # Limit total attempts
                    if results['passwords_tested'] > 10000:
                        return results
                    
                    for algo_name in algorithms[:2]:  # Limit algorithms
                        if algo_name.upper() in ['MD5', 'SHA1', 'SHA256']:
                            algo = self.hash_algorithms.get(algo_name.lower())
                            if algo:
                                if algo_name not in results['algorithms_tested']:
                                    results['algorithms_tested'].append(algo_name)
                                
                                computed_hash = algo(password.encode()).hexdigest().lower()
                                
                                if computed_hash == target_cleaned:
                                    results['found_matches'].append({
                                        'password': password,
                                        'algorithm': algo_name,
                                        'hash': computed_hash
                                    })
                                    self.log_info(f"Hash cracked: {password} ({algo_name})")
                                    return results
            
        except Exception as e:
            self.log_debug(f"Brute force attack error: {e}")
        
        return results
    
    def _assess_weaknesses(self, analysis_results):
        """Assess cryptographic weaknesses"""
        weaknesses = {
            'identified_weaknesses': [],
            'risk_level': 'unknown',
            'recommendations': []
        }
        
        try:
            # Check for weak algorithms
            likely_algos = analysis_results.get('hash_identification', {}).get('likely_algorithms', [])
            
            for algo in likely_algos:
                if algo.upper() in ['MD5', 'SHA1']:
                    weaknesses['identified_weaknesses'].append(f"{algo} is cryptographically broken")
                elif 'CRC32' in algo:
                    weaknesses['identified_weaknesses'].append("CRC32 is not cryptographically secure")
            
            # Check entropy
            entropy = analysis_results.get('entropy_analysis', {}).get('shannon_entropy', 0)
            if entropy < 4.0:
                weaknesses['identified_weaknesses'].append("Low entropy indicates weak randomness")
            
            # Check for patterns
            patterns = analysis_results.get('pattern_analysis', {})
            if patterns.get('repeated_sequences'):
                weaknesses['identified_weaknesses'].append("Repeated sequences detected")
            
            # Check if hash was cracked
            crack_results = analysis_results.get('crack_attempts', {})
            if crack_results.get('found_matches'):
                weaknesses['identified_weaknesses'].append("Hash successfully cracked")
            
            # Assess overall risk
            if len(weaknesses['identified_weaknesses']) >= 3:
                weaknesses['risk_level'] = 'high'
            elif len(weaknesses['identified_weaknesses']) >= 1:
                weaknesses['risk_level'] = 'medium'
            else:
                weaknesses['risk_level'] = 'low'
            
            # Generate recommendations
            if 'MD5' in str(likely_algos) or 'SHA1' in str(likely_algos):
                weaknesses['recommendations'].append("Migrate to SHA-256 or SHA-3")
            
            if entropy < 6.0:
                weaknesses['recommendations'].append("Use stronger random number generation")
            
            if crack_results.get('found_matches'):
                weaknesses['recommendations'].append("Use stronger passwords and salting")
            
            weaknesses['recommendations'].append("Consider using bcrypt, scrypt, or Argon2 for password hashing")
            
        except Exception as e:
            self.log_debug(f"Weakness assessment error: {e}")
        
        return weaknesses
    
    def _load_common_passwords(self):
        """Load common passwords for dictionary attacks"""
        return [
            "password", "123456", "password123", "admin", "qwerty", "letmein",
            "welcome", "monkey", "dragon", "master", "hello", "login", "guest",
            "admin123", "root", "test", "user", "pass", "secret", "default",
            "administrator", "password1", "12345", "1234", "123", "abc123",
            "password12", "sunshine", "princess", "football", "charlie", "freedom",
            "rainbow", "maggie", "jordan", "tigger", "superman", "harley",
            "1234567", "password1234", "trustno1", "batman", "thomas", "robert",
            "michael", "jennifer", "jordan23", "daniel", "hockey", "baseball"
        ]
    
    def _analyze_caesar(self, text):
        """Analyze for Caesar cipher"""
        results = {
            'likely_shifts': [],
            'best_candidates': []
        }
        
        # Try all possible shifts
        for shift in range(26):
            shifted = ""
            for char in text:
                if char.isalpha():
                    base = ord('A') if char.isupper() else ord('a')
                    shifted += chr((ord(char) - base + shift) % 26 + base)
                else:
                    shifted += char
            
            # Simple heuristic: check for common English words
            if self._looks_like_text(shifted):
                results['likely_shifts'].append(shift)
                results['best_candidates'].append({
                    'shift': shift,
                    'text': shifted[:100]  # Limit length
                })
        
        return results
    
    def _looks_like_text(self, text):
        """Simple heuristic to check if text looks like English"""
        common_words = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'man', 'men', 'say', 'she', 'too', 'use']
        text_lower = text.lower()
        word_count = sum(1 for word in common_words if word in text_lower)
        return word_count >= 2
    
    def _frequency_analysis(self, text):
        """Perform frequency analysis on text"""
        char_freq = {}
        text_alpha = ''.join(c.lower() for c in text if c.isalpha())
        
        for char in text_alpha:
            char_freq[char] = char_freq.get(char, 0) + 1
        
        total_chars = len(text_alpha)
        if total_chars == 0:
            return {}
        
        # Convert to percentages and sort
        freq_percent = {
            char: (count / total_chars) * 100 
            for char, count in char_freq.items()
        }
        
        return dict(sorted(freq_percent.items(), key=lambda x: x[1], reverse=True))
    
    def _check_alternating_pattern(self, data):
        """Check for alternating character patterns"""
        if len(data) < 4:
            return False
        
        patterns = []
        for i in range(min(4, len(data) - 1)):
            if i + 2 < len(data):
                if data[i] == data[i + 2]:
                    patterns.append(True)
                else:
                    patterns.append(False)
        
        return all(patterns) if patterns else False
    
    def _check_sequential_chars(self, data):
        """Check for sequential characters"""
        sequential_count = 0
        for i in range(len(data) - 1):
            if data[i].isalnum() and data[i + 1].isalnum():
                if abs(ord(data[i]) - ord(data[i + 1])) == 1:
                    sequential_count += 1
        
        return sequential_count >= 3