"""
Main CLI interface for Wolf cybersecurity toolkit
"""

import click
import json
import sys
from wolf import (
    wifi, subdomain, nslookup, ipinfo, dirbrute, csrf
)

@click.group()
@click.version_option(version='1.0.0', prog_name='wolf-cli')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
@click.pass_context
def cli(ctx, verbose, output):
    """
    Wolf - Advanced Cybersecurity and Ethical Hacking Toolkit
    
    A comprehensive toolkit for cybersecurity professionals and ethical hackers.
    """
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['output'] = output
    
    if verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)

@cli.command()
@click.option('--interface', '-i', help='Network interface to use')
@click.option('--target', '-t', help='Target network BSSID or SSID')
@click.option('--duration', '-d', default=30, help='Scan duration in seconds')
@click.pass_context
def wifi_scan(ctx, interface, target, duration):
    """Perform WiFi penetration testing operations"""
    click.echo("🔍 Starting WiFi scan...")
    
    try:
        results = wifi(interface=interface, target=target, duration=duration)
        
        if ctx.obj['output']:
            with open(ctx.obj['output'], 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"Results saved to {ctx.obj['output']}")
        else:
            _display_wifi_results(results)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

def _display_wifi_results(results):
    """Display WiFi scan results"""
    if 'error' in results:
        click.echo(f"❌ Error: {results['error']}")
        return
    
    click.echo(f"📡 Interface: {results.get('interface', 'Unknown')}")
    click.echo(f"🕐 Scan Duration: {results.get('scan_duration', 'Unknown')}s")
    click.echo(f"📊 Networks Found: {len(results.get('networks', []))}")
    click.echo("\n" + "="*60)
    
    for i, network in enumerate(results.get('networks', []), 1):
        click.echo(f"\n🌐 Network {i}:")
        click.echo(f"   SSID: {network.get('ssid', 'Hidden')}")
        click.echo(f"   BSSID: {network.get('bssid', 'Unknown')}")
        click.echo(f"   Security: {network.get('security', 'Unknown')}")
        click.echo(f"   Signal: {network.get('signal', 'Unknown')}")
        click.echo(f"   Quality: {network.get('quality', 'Unknown')}")

@cli.command()
@click.argument('domain')
@click.option('--wordlist', '-w', type=click.Path(exists=True), help='Custom wordlist file')
@click.option('--threads', '-t', default=10, help='Number of threads')
@click.option('--timeout', default=5, help='Request timeout in seconds')
@click.pass_context
def subdomain_enum(ctx, domain, wordlist, threads, timeout):
    """Enumerate subdomains for a given domain"""
    click.echo(f"🔍 Enumerating subdomains for {domain}...")
    
    try:
        results = subdomain(domain=domain, wordlist=wordlist, threads=threads, timeout=timeout)
        
        if ctx.obj['output']:
            with open(ctx.obj['output'], 'w') as f:
                json.dump({'domain': domain, 'subdomains': results}, f, indent=2)
            click.echo(f"Results saved to {ctx.obj['output']}")
        else:
            _display_subdomain_results(domain, results)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

def _display_subdomain_results(domain, results):
    """Display subdomain enumeration results"""
    click.echo(f"🎯 Target: {domain}")
    click.echo(f"📊 Subdomains Found: {len(results)}")
    click.echo("\n" + "="*50)
    
    for subdomain in results:
        click.echo(f"✅ {subdomain}")

@cli.command()
@click.argument('domain')
@click.option('--type', '-t', default='A', help='DNS record type')
@click.option('--nameserver', '-ns', help='Specific nameserver to use')
@click.pass_context
def dns_lookup(ctx, domain, type, nameserver):
    """Perform DNS lookup operations"""
    click.echo(f"🔍 Performing DNS lookup for {domain} ({type} records)...")
    
    try:
        results = nslookup(domain=domain, record_type=type, nameserver=nameserver)
        
        if ctx.obj['output']:
            with open(ctx.obj['output'], 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"Results saved to {ctx.obj['output']}")
        else:
            _display_dns_results(results)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

def _display_dns_results(results):
    """Display DNS lookup results"""
    click.echo(f"🎯 Domain: {results.get('domain')}")
    click.echo(f"📋 Record Type: {results.get('record_type')}")
    click.echo(f"🌐 Nameserver: {results.get('nameserver')}")
    
    if 'error' in results:
        click.echo(f"❌ Error: {results['error']}")
        return
    
    click.echo(f"📊 Records Found: {len(results.get('records', []))}")
    click.echo("\n" + "="*50)
    
    for record in results.get('records', []):
        click.echo(f"✅ {record.get('data')}")
        if 'ttl' in record:
            click.echo(f"   TTL: {record['ttl']}")

@cli.command()
@click.argument('target')
@click.option('--geolocation/--no-geolocation', default=True, help='Include geolocation data')
@click.option('--whois/--no-whois', default=True, help='Include WHOIS data')
@click.pass_context
def ip_info(ctx, target, geolocation, whois):
    """Gather IP and domain information"""
    click.echo(f"🔍 Gathering information for {target}...")
    
    try:
        results = ipinfo(
            target=target,
            include_geolocation=geolocation,
            include_whois=whois
        )
        
        if ctx.obj['output']:
            with open(ctx.obj['output'], 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"Results saved to {ctx.obj['output']}")
        else:
            _display_ipinfo_results(results)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

def _display_ipinfo_results(results):
    """Display IP information results"""
    click.echo(f"🎯 Target: {results.get('target')}")
    click.echo(f"📋 Type: {results.get('target_type')}")
    
    if 'error' in results:
        click.echo(f"❌ Error: {results['error']}")
        return
    
    # Basic info
    basic_info = results.get('basic_info', {})
    if basic_info:
        click.echo("\n📋 Basic Information:")
        click.echo("-" * 30)
        for key, value in basic_info.items():
            click.echo(f"   {key}: {value}")
    
    # Geolocation
    geolocation = results.get('geolocation', {})
    if geolocation:
        click.echo("\n🌍 Geolocation:")
        click.echo("-" * 30)
        for key, value in geolocation.items():
            if value:
                click.echo(f"   {key}: {value}")
    
    # Network info
    network_info = results.get('network_info', {})
    if network_info.get('open_ports'):
        click.echo("\n🔌 Open Ports:")
        click.echo("-" * 30)
        click.echo(f"   {', '.join(map(str, network_info['open_ports']))}")

@cli.command()
@click.argument('url')
@click.option('--wordlist', '-w', type=click.Path(exists=True), help='Custom wordlist file')
@click.option('--threads', '-t', default=10, help='Number of threads')
@click.option('--extensions', '-e', help='File extensions (comma-separated)')
@click.option('--recursive', '-r', is_flag=True, help='Recursive directory scanning')
@click.pass_context
def dir_brute(ctx, url, wordlist, threads, extensions, recursive):
    """Perform directory brute-force attacks"""
    click.echo(f"🔍 Starting directory brute-force on {url}...")
    
    # Parse extensions
    ext_list = None
    if extensions:
        ext_list = [ext.strip() for ext in extensions.split(',')]
    
    try:
        if recursive:
            results = dirbrute(url, wordlist=wordlist, threads=threads, extensions=ext_list)
            # For simplicity, using regular brute force here
            # In a full implementation, you'd call a recursive method
        else:
            results = dirbrute(url=url, wordlist=wordlist, threads=threads, extensions=ext_list)
        
        if ctx.obj['output']:
            with open(ctx.obj['output'], 'w') as f:
                json.dump({'url': url, 'found_paths': results}, f, indent=2)
            click.echo(f"Results saved to {ctx.obj['output']}")
        else:
            _display_dirbrute_results(url, results)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

def _display_dirbrute_results(url, results):
    """Display directory brute-force results"""
    click.echo(f"🎯 Target: {url}")
    click.echo(f"📊 Paths Found: {len(results)}")
    click.echo("\n" + "="*70)
    
    for path_info in results:
        status_emoji = "✅" if path_info['status_code'] == 200 else "🔄"
        click.echo(f"{status_emoji} {path_info['path']} ({path_info['status_code']}) - {path_info['content_length']} bytes")

@cli.command()
@click.argument('url')
@click.option('--advanced', '-a', is_flag=True, help='Perform advanced CSRF testing')
@click.pass_context
def csrf_test(ctx, url, advanced):
    """Test for CSRF vulnerabilities"""
    click.echo(f"🔍 Testing CSRF vulnerabilities on {url}...")
    
    try:
        if advanced:
            # In full implementation, this would call an advanced method
            results = csrf(url=url)
        else:
            results = csrf(url=url)
        
        if ctx.obj['output']:
            with open(ctx.obj['output'], 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"Results saved to {ctx.obj['output']}")
        else:
            _display_csrf_results(results)
            
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)

def _display_csrf_results(results):
    """Display CSRF test results"""
    click.echo(f"🎯 Target: {results.get('url')}")
    click.echo(f"📋 Forms Found: {results.get('forms_found', 0)}")
    click.echo(f"🔒 CSRF Tokens Found: {results.get('csrf_tokens_found', 0)}")
    click.echo(f"⚠️  Vulnerable Forms: {len(results.get('vulnerable_forms', []))}")
    click.echo(f"🚨 Risk Level: {results.get('risk_level', 'Unknown')}")
    
    if 'error' in results:
        click.echo(f"❌ Error: {results['error']}")
        return
    
    # Show vulnerable forms
    vulnerable_forms = results.get('vulnerable_forms', [])
    if vulnerable_forms:
        click.echo("\n⚠️  Vulnerable Forms:")
        click.echo("-" * 50)
        for i, form in enumerate(vulnerable_forms, 1):
            click.echo(f"   Form {i}: {form.get('action', 'Unknown action')}")
            click.echo(f"   Method: {form.get('method', 'Unknown')}")
            click.echo(f"   Reasons: {', '.join(form.get('vulnerability_reasons', []))}")
            click.echo()
    
    # Show recommendations
    recommendations = results.get('recommendations', [])
    if recommendations:
        click.echo("💡 Recommendations:")
        click.echo("-" * 50)
        for rec in recommendations:
            click.echo(f"   • {rec}")

if __name__ == '__main__':
    cli()
