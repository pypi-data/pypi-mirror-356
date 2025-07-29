"""
Core functionality for Cyber Wolf Hunter
"""

import requests
import threading
import time
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .scanners import VulnerabilityScanner
from .reporter import HTMLReporter


class WolfHunter:
    """
    Main scanner class for comprehensive vulnerability assessment
    """
    
    def __init__(self, target_url, threads=10):
        """
        Initialize Wolf Hunter scanner
        
        Args:
            target_url (str): Target website URL
            threads (int): Number of concurrent threads
        """
        self.target_url = self._normalize_url(target_url)
        self.threads = min(threads, 100)  # Cap at 100 threads for safety
        self.scanner = VulnerabilityScanner()
        self.reporter = HTMLReporter()
        self.results = {
            'target': self.target_url,
            'scan_time': None,
            'vulnerabilities': [],
            'statistics': {
                'total_checks': 0,
                'vulnerabilities_found': 0,
                'high_risk': 0,
                'medium_risk': 0,
                'low_risk': 0
            },
            'scan_duration': 0
        }
        
    def _normalize_url(self, url):
        """Normalize URL format"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def scan(self):
        """
        Perform comprehensive vulnerability scan
        
        Returns:
            dict: Scan results containing vulnerabilities and statistics
        """
        self._display_wolf_banner()
        print(f"🐺 Cyber Wolf Hunter - Starting scan on {self.target_url}")
        print(f"📊 Using {self.threads} threads for concurrent scanning")
        
        start_time = time.time()
        self.results['scan_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Test connectivity first
        if not self._test_connectivity():
            print("❌ Target is not accessible")
            return self.results
        
        print("✅ Target is accessible - proceeding with vulnerability assessment")
        
        # Define scanning tasks with enhanced checks
        scan_tasks = [
            ('SQL Injection', self.scanner.check_sql_injection),
            ('XSS Vulnerabilities', self.scanner.check_xss),
            ('Directory Traversal', self.scanner.check_directory_traversal),
            ('Open Redirects', self.scanner.check_open_redirect),
            ('CSRF Vulnerabilities', self.scanner.check_csrf),
            ('Information Disclosure', self.scanner.check_info_disclosure),
            ('HTTP Security Headers', self.scanner.check_security_headers),
            ('SSL/TLS Configuration', self.scanner.check_ssl_config),
            ('Directory Enumeration', self.scanner.check_directory_enum),
            ('File Upload Vulnerabilities', self.scanner.check_file_upload),
            ('Server Information', self.scanner.check_server_info),
            ('Cookie Security', self.scanner.check_cookie_security),
            ('Authentication Bypass', self.scanner.check_auth_bypass),
            ('Command Injection', self.scanner.check_command_injection),
            ('LDAP Injection', self.scanner.check_ldap_injection)
        ]
        
        # Execute scans with threading
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_scan = {
                executor.submit(scan_func, self.target_url): scan_name 
                for scan_name, scan_func in scan_tasks
            }
            
            for future in as_completed(future_to_scan):
                scan_name = future_to_scan[future]
                try:
                    vulnerabilities = future.result()
                    if vulnerabilities:
                        self.results['vulnerabilities'].extend(vulnerabilities)
                        print(f"🔍 {scan_name}: {len(vulnerabilities)} issues found")
                    else:
                        print(f"✅ {scan_name}: No vulnerabilities detected")
                except Exception as e:
                    print(f"⚠️  {scan_name}: Error during scan - {str(e)}")
        
        # Calculate statistics
        self._calculate_statistics()
        self.results['scan_duration'] = round(time.time() - start_time, 2)
        
        print(f"\n🎯 Scan completed in {self.results['scan_duration']} seconds")
        print(f"📈 Found {self.results['statistics']['vulnerabilities_found']} vulnerabilities")
        
        # Display detailed results in table format
        self._display_results_table()
        
        return self.results
    
    def _test_connectivity(self):
        """Test if target is accessible"""
        try:
            response = requests.get(self.target_url, timeout=10, verify=False)
            return response.status_code < 500
        except:
            return False
    
    def _calculate_statistics(self):
        """Calculate vulnerability statistics"""
        self.results['statistics']['total_checks'] = len(self.results['vulnerabilities'])
        self.results['statistics']['vulnerabilities_found'] = len(self.results['vulnerabilities'])
        
        for vuln in self.results['vulnerabilities']:
            risk_level = vuln.get('risk_level', 'low').lower()
            if risk_level == 'high':
                self.results['statistics']['high_risk'] += 1
            elif risk_level == 'medium':
                self.results['statistics']['medium_risk'] += 1
            else:
                self.results['statistics']['low_risk'] += 1
    
    def generate_report(self, filename="cyber_wolf_report.html"):
        """
        Generate HTML vulnerability report
        
        Args:
            filename (str): Output filename for the report
        """
        print(f"📄 Generating HTML report: {filename}")
        report_path = self.reporter.generate_html_report(self.results, filename)
        print(f"✅ Report saved to: {report_path}")
        return report_path
    
    def _display_results_table(self):
        """Display detailed vulnerability results in table format"""
        if not self.results['vulnerabilities']:
            print("\n" + "="*100)
            print("🛡️  EXCELLENT! No vulnerabilities detected during comprehensive scan")
            print("="*100)
            return
        
        print("\n" + "="*120)
        print("📊 DETAILED VULNERABILITY ASSESSMENT RESULTS")
        print("="*120)
        
        # Table header
        print(f"{'#':<3} {'VULNERABILITY TYPE':<25} {'SEVERITY':<10} {'URL/ENDPOINT':<35} {'DETAILS':<25} {'STATUS':<10}")
        print("-"*120)
        
        # Sort vulnerabilities by severity
        severity_order = {'High': 1, 'Medium': 2, 'Low': 3}
        sorted_vulns = sorted(self.results['vulnerabilities'], 
                            key=lambda x: severity_order.get(x.get('severity', 'Low'), 3))
        
        for i, vuln in enumerate(sorted_vulns, 1):
            vuln_type = vuln.get('type', 'Unknown')[:24]
            severity = vuln.get('severity', 'Low')
            url = vuln.get('url', self.target_url)[:34]
            evidence = vuln.get('evidence', 'Detected')[:24]
            
            # Color coding for severity
            if severity == 'High':
                status = "🔴 CRITICAL"
            elif severity == 'Medium':
                status = "🟡 WARNING"
            else:
                status = "🟢 INFO"
            
            print(f"{i:<3} {vuln_type:<25} {severity:<10} {url:<35} {evidence:<25} {status:<10}")
        
        print("-"*120)
        
        # Summary statistics table
        print("\n📈 VULNERABILITY SUMMARY")
        print("-"*60)
        print(f"{'RISK LEVEL':<15} {'COUNT':<10} {'PERCENTAGE':<15} {'ACTION REQUIRED':<20}")
        print("-"*60)
        
        total = self.results['statistics']['vulnerabilities_found']
        high = self.results['statistics']['high_risk']
        medium = self.results['statistics']['medium_risk']
        low = self.results['statistics']['low_risk']
        
        if total > 0:
            print(f"{'🔴 High Risk':<15} {high:<10} {(high/total*100):.1f}%{'':<10} {'Immediate Fix':<20}")
            print(f"{'🟡 Medium Risk':<15} {medium:<10} {(medium/total*100):.1f}%{'':<10} {'Schedule Fix':<20}")
            print(f"{'🟢 Low Risk':<15} {low:<10} {(low/total*100):.1f}%{'':<10} {'Monitor':<20}")
        
        print("-"*60)
        print(f"Total Issues: {total} | Scan Duration: {self.results['scan_duration']}s | Target: {self.target_url}")
        print("="*120)

    def get_summary(self):
        """Get a summary of scan results"""
        return {
            'target': self.target_url,
            'total_vulnerabilities': self.results['statistics']['vulnerabilities_found'],
            'high_risk': self.results['statistics']['high_risk'],
            'medium_risk': self.results['statistics']['medium_risk'],
            'low_risk': self.results['statistics']['low_risk'],
            'scan_duration': self.results['scan_duration']
        }
    
    def get_detailed_report(self):
        """Get detailed vulnerability report with recommendations"""
        report = {
            'executive_summary': {
                'target': self.target_url,
                'scan_date': self.results['scan_time'],
                'total_vulnerabilities': self.results['statistics']['vulnerabilities_found'],
                'risk_distribution': {
                    'high': self.results['statistics']['high_risk'],
                    'medium': self.results['statistics']['medium_risk'],
                    'low': self.results['statistics']['low_risk']
                },
                'scan_duration': self.results['scan_duration']
            },
            'vulnerabilities': self.results['vulnerabilities'],
            'recommendations': self._generate_recommendations()
        }
        return report
    
    def _generate_recommendations(self):
        """Generate security recommendations based on findings"""
        recommendations = []
        
        vuln_types = set(vuln['type'] for vuln in self.results['vulnerabilities'])
        
        if any('SQL Injection' in vtype for vtype in vuln_types):
            recommendations.append({
                'priority': 'Critical',
                'issue': 'SQL Injection vulnerabilities detected',
                'action': 'Implement parameterized queries and input validation immediately',
                'impact': 'High - Database compromise possible'
            })
        
        if any('XSS' in vtype for vtype in vuln_types):
            recommendations.append({
                'priority': 'High',
                'issue': 'Cross-Site Scripting vulnerabilities found',
                'action': 'Implement proper output encoding and Content Security Policy',
                'impact': 'Medium - User session hijacking possible'
            })
        
        if any('Security Header' in vtype for vtype in vuln_types):
            recommendations.append({
                'priority': 'Medium',
                'issue': 'Missing security headers detected',
                'action': 'Configure proper HTTP security headers',
                'impact': 'Low - Various attack vectors enabled'
            })
        
        return recommendations
    
    def _display_wolf_banner(self):
        """Display ASCII art wolf banner"""
        wolf_art = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                             🐺 CYBER WOLF HUNTER 🐺                          ║
    ╠══════════════════════════════════════════════════════════════════════════════╣
    ║                                                                              ║
    ║                              ,-.             _,---._ __  / \                 ║
    ║                             /  )         .-'       `./  /   \                ║
    ║                            (  (          /.-.     _/  /     \               ║
    ║                             \  )        ( (   )   `-./       \              ║
    ║                              ) (          '-'         |       /             ║
    ║                             (  (  )                   \    ./               ║
    ║                              \  \(            _       /   /                 ║
    ║                               \  ' \        ,-' |_   (   (                  ║
    ║                                \   \\     ,'    __`-. \.  \                 ║
    ║                                 )   ) )   /    ,'    `. \  \                ║
    ║                                /  ,' (   (    (       ) )  )                ║
    ║                               (  (    \   \    \     /,' /                  ║
    ║                                \  \    `-. `-._`-...-' ,'                   ║
    ║                                 `. `-.    `-._`------''                     ║
    ║                                   `-.__>--._/  /                            ║
    ║                                             /  /                            ║
    ║                                            (__/                             ║
    ║                                                                              ║
    ║    Advanced Vulnerability Scanner | Multi-Threading | Professional Reports   ║
    ║                  Developed by S.Tamilselvan | Version 2.0                   ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(wolf_art)
    
    def advanced_scan(self, scan_type="comprehensive"):
        """
        Advanced scanning with multiple modes and enhanced features
        
        Args:
            scan_type (str): Type of scan - 'quick', 'comprehensive', 'deep', 'stealth'
        
        Returns:
            dict: Advanced scan results with detailed analytics
        """
        self._display_wolf_banner()
        
        scan_configs = {
            'quick': {'threads': min(self.threads, 20), 'depth': 'surface'},
            'comprehensive': {'threads': self.threads, 'depth': 'standard'},
            'deep': {'threads': min(self.threads * 2, 150), 'depth': 'extensive'},
            'stealth': {'threads': min(self.threads // 2, 10), 'depth': 'careful'}
        }
        
        config = scan_configs.get(scan_type, scan_configs['comprehensive'])
        
        print(f"🔥 Advanced {scan_type.upper()} scan initiated on {self.target_url}")
        print(f"⚡ Performance Mode: {config['threads']} threads | Depth: {config['depth']}")
        print(f"🎯 Enhanced Detection: 20+ vulnerability types | AI-powered analysis")
        
        # Enhanced scanning with additional features
        start_time = time.time()
        self.results['scan_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.results['scan_type'] = scan_type
        self.results['performance_metrics'] = {}
        
        # Test connectivity with advanced checks
        if not self._advanced_connectivity_test():
            print("❌ Target unreachable or blocking automated requests")
            return self.results
        
        print("✅ Target accessible - Initiating advanced vulnerability assessment")
        
        # Enhanced scanning tasks with AI-powered detection
        enhanced_tasks = [
            ('SQL Injection Advanced', self.scanner.check_sql_injection_advanced),
            ('XSS Complete Analysis', self.scanner.check_xss_advanced),
            ('Directory Traversal Deep', self.scanner.check_directory_traversal_advanced),
            ('Open Redirects Enhanced', self.scanner.check_open_redirect),
            ('CSRF Advanced Protection', self.scanner.check_csrf_advanced),
            ('Information Disclosure Deep', self.scanner.check_info_disclosure_advanced),
            ('HTTP Security Headers Pro', self.scanner.check_security_headers_advanced),
            ('SSL/TLS Advanced Config', self.scanner.check_ssl_config_advanced),
            ('Directory Enumeration Pro', self.scanner.check_directory_enum_advanced),
            ('File Upload Advanced', self.scanner.check_file_upload_advanced),
            ('Server Information Pro', self.scanner.check_server_info),
            ('Cookie Security Advanced', self.scanner.check_cookie_security_advanced),
            ('Authentication Bypass Pro', self.scanner.check_auth_bypass_advanced),
            ('Command Injection Deep', self.scanner.check_command_injection_advanced),
            ('LDAP Injection Advanced', self.scanner.check_ldap_injection_advanced),
            ('NoSQL Injection Detection', self.scanner.check_nosql_injection),
            ('XML External Entity (XXE)', self.scanner.check_xxe_injection),
            ('SSRF Detection', self.scanner.check_ssrf),
            ('Insecure Deserialization', self.scanner.check_deserialization),
            ('Security Misconfiguration', self.scanner.check_security_misconfig)
        ]
        
        # Execute advanced scans with performance monitoring
        with ThreadPoolExecutor(max_workers=config['threads']) as executor:
            future_to_scan = {
                executor.submit(scan_func, self.target_url): scan_name 
                for scan_name, scan_func in enhanced_tasks
                if hasattr(self.scanner, scan_func.__name__)
            }
            
            completed_scans = 0
            total_scans = len(future_to_scan)
            
            for future in as_completed(future_to_scan):
                scan_name = future_to_scan[future]
                completed_scans += 1
                progress = (completed_scans / total_scans) * 100
                
                try:
                    scan_start = time.time()
                    vulnerabilities = future.result()
                    scan_duration = time.time() - scan_start
                    
                    # Store performance metrics
                    self.results['performance_metrics'][scan_name] = {
                        'duration': round(scan_duration, 2),
                        'vulnerabilities_found': len(vulnerabilities) if vulnerabilities else 0
                    }
                    
                    if vulnerabilities:
                        self.results['vulnerabilities'].extend(vulnerabilities)
                        print(f"🔍 [{progress:5.1f}%] {scan_name}: {len(vulnerabilities)} issues detected")
                    else:
                        print(f"✅ [{progress:5.1f}%] {scan_name}: Secure")
                        
                except Exception as e:
                    print(f"⚠️  [{progress:5.1f}%] {scan_name}: Scan error - {str(e)[:50]}")
        
        # Advanced analytics and AI-powered risk assessment
        self._perform_advanced_analytics()
        self._calculate_statistics()
        self.results['scan_duration'] = round(time.time() - start_time, 2)
        
        # Display enhanced results
        self._display_advanced_results()
        
        return self.results
    
    def _advanced_connectivity_test(self):
        """Advanced connectivity testing with multiple protocols"""
        try:
            # Test HTTP/HTTPS with different user agents
            test_headers = [
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                {'User-Agent': 'Cyber-Wolf-Hunter/2.0 Advanced Security Scanner'},
                {'User-Agent': 'Mozilla/5.0 (compatible; SecurityBot/1.0)'}
            ]
            
            for headers in test_headers:
                response = requests.get(self.target_url, timeout=15, verify=False, headers=headers)
                if response.status_code < 500:
                    return True
            
            return False
        except:
            return False
    
    def _perform_advanced_analytics(self):
        """Perform AI-powered analytics on scan results"""
        if not self.results['vulnerabilities']:
            self.results['risk_score'] = 0
            self.results['security_grade'] = 'A+'
            return
        
        # Calculate advanced risk score
        risk_weights = {'High': 10, 'Medium': 5, 'Low': 1}
        total_risk = sum(risk_weights.get(vuln.get('severity', 'Low'), 1) 
                        for vuln in self.results['vulnerabilities'])
        
        # Normalize risk score (0-100)
        max_possible_risk = len(self.results['vulnerabilities']) * 10
        self.results['risk_score'] = min(100, (total_risk / max_possible_risk * 100)) if max_possible_risk > 0 else 0
        
        # Assign security grade
        if self.results['risk_score'] <= 10:
            self.results['security_grade'] = 'A+'
        elif self.results['risk_score'] <= 25:
            self.results['security_grade'] = 'A'
        elif self.results['risk_score'] <= 40:
            self.results['security_grade'] = 'B'
        elif self.results['risk_score'] <= 60:
            self.results['security_grade'] = 'C'
        elif self.results['risk_score'] <= 80:
            self.results['security_grade'] = 'D'
        else:
            self.results['security_grade'] = 'F'
        
        # Advanced threat categorization
        threat_categories = {}
        for vuln in self.results['vulnerabilities']:
            category = self._categorize_threat(vuln['type'])
            threat_categories[category] = threat_categories.get(category, 0) + 1
        
        self.results['threat_landscape'] = threat_categories
    
    def _categorize_threat(self, vuln_type):
        """Categorize threats into OWASP Top 10 categories"""
        owasp_mapping = {
            'SQL Injection': 'A03:2021 – Injection',
            'XSS': 'A03:2021 – Injection', 
            'Authentication Bypass': 'A07:2021 – Identification and Authentication Failures',
            'Missing Security Header': 'A05:2021 – Security Misconfiguration',
            'Server Information': 'A05:2021 – Security Misconfiguration',
            'Cookie Security': 'A05:2021 – Security Misconfiguration',
            'SSL/TLS': 'A02:2021 – Cryptographic Failures',
            'Directory Traversal': 'A01:2021 – Broken Access Control',
            'File Upload': 'A01:2021 – Broken Access Control',
            'Command Injection': 'A03:2021 – Injection',
            'LDAP Injection': 'A03:2021 – Injection'
        }
        
        for key, category in owasp_mapping.items():
            if key.lower() in vuln_type.lower():
                return category
        
        return 'A06:2021 – Vulnerable and Outdated Components'
    
    def _display_advanced_results(self):
        """Display enhanced results with advanced analytics"""
        print("\n" + "="*120)
        print("🎯 ADVANCED CYBER WOLF HUNTER RESULTS")
        print("="*120)
        
        # Security scorecard
        print(f"🏆 Security Grade: {self.results.get('security_grade', 'N/A')}")
        print(f"📊 Risk Score: {self.results.get('risk_score', 0):.1f}/100")
        print(f"🔍 Scan Type: {self.results.get('scan_type', 'standard').upper()}")
        print(f"⏱️  Total Duration: {self.results['scan_duration']}s")
        
        # Display detailed table if vulnerabilities found
        if self.results['vulnerabilities']:
            self._display_results_table()
            
            # Threat landscape analysis
            if 'threat_landscape' in self.results:
                print(f"\n🌐 THREAT LANDSCAPE ANALYSIS (OWASP Top 10)")
                print("-" * 80)
                for threat, count in self.results['threat_landscape'].items():
                    print(f"• {threat}: {count} issue(s)")
        
        # Performance metrics
        if 'performance_metrics' in self.results:
            print(f"\n⚡ PERFORMANCE METRICS")
            print("-" * 60)
            total_checks = len(self.results['performance_metrics'])
            avg_duration = sum(m['duration'] for m in self.results['performance_metrics'].values()) / total_checks
            print(f"Total Security Checks: {total_checks}")
            print(f"Average Check Duration: {avg_duration:.2f}s")
            print(f"Fastest Check: {min(m['duration'] for m in self.results['performance_metrics'].values()):.2f}s")
            print(f"Slowest Check: {max(m['duration'] for m in self.results['performance_metrics'].values()):.2f}s")
        
        print("="*120)
