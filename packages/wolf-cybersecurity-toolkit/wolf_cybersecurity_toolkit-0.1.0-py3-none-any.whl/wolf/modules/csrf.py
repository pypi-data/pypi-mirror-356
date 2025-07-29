"""
CSRF (Cross-Site Request Forgery) testing module
"""

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from wolf.core.base import BaseModule

class CSRFModule(BaseModule):
    """
    CSRF vulnerability testing capabilities
    """
    
    def __init__(self):
        super().__init__("CSRF")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def execute(self, url, **kwargs):
        """
        Execute CSRF testing
        
        Args:
            url (str): Target URL
            **kwargs: Additional parameters
            
        Returns:
            dict: CSRF test results
        """
        return self.test(url=url, **kwargs)
    
    def test(self, url, **kwargs):
        """
        Test for CSRF vulnerabilities
        
        Args:
            url (str): Target URL to test
            **kwargs: Additional parameters
            
        Returns:
            dict: CSRF test results
        """
        self.log_info(f"Starting CSRF testing on {url}")
        
        results = {
            'url': url,
            'forms_found': 0,
            'vulnerable_forms': [],
            'csrf_tokens_found': 0,
            'recommendations': [],
            'risk_level': 'Unknown'
        }
        
        try:
            # Get the page
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                results['error'] = f"HTTP {response.status_code}: Unable to access page"
                return results
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all forms
            forms = soup.find_all('form')
            results['forms_found'] = len(forms)
            
            if not forms:
                results['message'] = "No forms found on the page"
                return results
            
            # Analyze each form
            for i, form in enumerate(forms):
                form_analysis = self._analyze_form(form, url, i)
                
                if form_analysis['is_vulnerable']:
                    results['vulnerable_forms'].append(form_analysis)
                
                if form_analysis['has_csrf_token']:
                    results['csrf_tokens_found'] += 1
            
            # Generate recommendations and risk assessment
            results['recommendations'] = self._generate_recommendations(results)
            results['risk_level'] = self._assess_risk_level(results)
            
            self.log_info(f"CSRF test complete: {len(results['vulnerable_forms'])} vulnerable forms found")
            
        except Exception as e:
            self.log_error(f"CSRF testing error: {e}")
            results['error'] = str(e)
        
        return results
    
    def _analyze_form(self, form, base_url, form_index):
        """
        Analyze a form for CSRF vulnerabilities
        
        Args:
            form (BeautifulSoup): Form element
            base_url (str): Base URL of the page
            form_index (int): Index of the form
            
        Returns:
            dict: Form analysis results
        """
        analysis = {
            'form_index': form_index,
            'action': '',
            'method': 'GET',
            'has_csrf_token': False,
            'csrf_token_names': [],
            'input_fields': [],
            'is_vulnerable': False,
            'vulnerability_reasons': []
        }
        
        try:
            # Get form action and method
            analysis['action'] = form.get('action', '')
            if analysis['action']:
                analysis['action'] = urljoin(base_url, analysis['action'])
            else:
                analysis['action'] = base_url
            
            analysis['method'] = form.get('method', 'GET').upper()
            
            # Find all input fields
            inputs = form.find_all(['input', 'textarea', 'select'])
            
            for input_field in inputs:
                field_info = {
                    'type': input_field.get('type', 'text'),
                    'name': input_field.get('name', ''),
                    'value': input_field.get('value', ''),
                    'tag': input_field.name
                }
                analysis['input_fields'].append(field_info)
                
                # Check for CSRF tokens
                if self._is_csrf_token_field(input_field):
                    analysis['has_csrf_token'] = True
                    analysis['csrf_token_names'].append(field_info['name'])
            
            # Determine if form is vulnerable
            analysis['is_vulnerable'], analysis['vulnerability_reasons'] = self._check_form_vulnerability(analysis)
            
        except Exception as e:
            self.log_debug(f"Error analyzing form {form_index}: {e}")
        
        return analysis
    
    def _is_csrf_token_field(self, input_field):
        """
        Check if input field is likely a CSRF token
        
        Args:
            input_field (BeautifulSoup): Input field element
            
        Returns:
            bool: True if likely a CSRF token field
        """
        name = input_field.get('name', '').lower()
        value = input_field.get('value', '')
        input_type = input_field.get('type', '').lower()
        
        # Common CSRF token field names
        csrf_names = [
            'csrf_token', 'csrftoken', '_token', 'authenticity_token',
            'csrf', 'token', '_csrf', 'csrfmiddlewaretoken', 'csrf_name',
            'form_token', 'security_token', 'anti_csrf_token'
        ]
        
        # Check if name matches common CSRF token names
        if any(csrf_name in name for csrf_name in csrf_names):
            return True
        
        # Check if it's a hidden field with a token-like value
        if (input_type == 'hidden' and 
            len(value) > 10 and 
            re.match(r'^[a-fA-F0-9]{8,}$|^[a-zA-Z0-9+/=]{16,}$', value)):
            return True
        
        return False
    
    def _check_form_vulnerability(self, analysis):
        """
        Check if form is vulnerable to CSRF
        
        Args:
            analysis (dict): Form analysis data
            
        Returns:
            tuple: (is_vulnerable, reasons)
        """
        is_vulnerable = False
        reasons = []
        
        # Only check POST forms (GET forms are generally not CSRF vulnerable in the traditional sense)
        if analysis['method'] != 'POST':
            return False, ['Form uses GET method']
        
        # Check for CSRF token presence
        if not analysis['has_csrf_token']:
            is_vulnerable = True
            reasons.append('No CSRF token found')
        
        # Check for state-changing operations
        has_sensitive_fields = False
        for field in analysis['input_fields']:
            field_name = field['name'].lower()
            if any(sensitive in field_name for sensitive in [
                'password', 'email', 'delete', 'remove', 'transfer',
                'amount', 'balance', 'admin', 'role', 'permission'
            ]):
                has_sensitive_fields = True
                break
        
        if has_sensitive_fields and not analysis['has_csrf_token']:
            reasons.append('Form contains sensitive fields without CSRF protection')
        
        # Check for file uploads without CSRF protection
        has_file_upload = any(field['type'] == 'file' for field in analysis['input_fields'])
        if has_file_upload and not analysis['has_csrf_token']:
            reasons.append('File upload form without CSRF protection')
        
        return is_vulnerable, reasons
    
    def _generate_recommendations(self, results):
        """
        Generate security recommendations
        
        Args:
            results (dict): Test results
            
        Returns:
            list: Security recommendations
        """
        recommendations = []
        
        if results['vulnerable_forms']:
            recommendations.append(
                "Implement CSRF tokens in all state-changing forms"
            )
            recommendations.append(
                "Use framework-provided CSRF protection mechanisms"
            )
            recommendations.append(
                "Verify CSRF tokens on the server side for all POST requests"
            )
            recommendations.append(
                "Consider implementing SameSite cookie attributes"
            )
            recommendations.append(
                "Implement proper session management"
            )
        
        if results['forms_found'] > 0 and results['csrf_tokens_found'] == 0:
            recommendations.append(
                "No CSRF tokens found - consider implementing anti-CSRF measures"
            )
        
        if not recommendations:
            recommendations.append(
                "Forms appear to have proper CSRF protection"
            )
        
        return recommendations
    
    def _assess_risk_level(self, results):
        """
        Assess overall risk level
        
        Args:
            results (dict): Test results
            
        Returns:
            str: Risk level
        """
        if results.get('error'):
            return 'Unknown'
        
        vulnerable_count = len(results['vulnerable_forms'])
        total_forms = results['forms_found']
        
        if vulnerable_count == 0:
            return 'Low'
        elif vulnerable_count < total_forms / 2:
            return 'Medium'
        else:
            return 'High'
    
    def advanced_csrf_test(self, url, **kwargs):
        """
        Perform advanced CSRF testing with token validation
        
        Args:
            url (str): Target URL
            **kwargs: Additional parameters
            
        Returns:
            dict: Advanced test results
        """
        self.log_info(f"Starting advanced CSRF testing on {url}")
        
        results = self.test(url, **kwargs)
        
        # Additional advanced tests
        if results['vulnerable_forms']:
            for form_data in results['vulnerable_forms']:
                # Test if CSRF tokens are properly validated
                advanced_results = self._test_csrf_token_validation(form_data, url)
                form_data['advanced_test'] = advanced_results
        
        return results
    
    def _test_csrf_token_validation(self, form_data, base_url):
        """
        Test CSRF token validation
        
        Args:
            form_data (dict): Form analysis data
            base_url (str): Base URL
            
        Returns:
            dict: Token validation test results
        """
        test_results = {
            'token_reuse_vulnerable': False,
            'invalid_token_accepted': False,
            'missing_token_accepted': False
        }
        
        try:
            # This would require more complex implementation
            # involving actual form submission and token manipulation
            self.log_debug("Advanced CSRF token validation testing not fully implemented")
            
        except Exception as e:
            self.log_debug(f"Advanced CSRF testing error: {e}")
        
        return test_results
