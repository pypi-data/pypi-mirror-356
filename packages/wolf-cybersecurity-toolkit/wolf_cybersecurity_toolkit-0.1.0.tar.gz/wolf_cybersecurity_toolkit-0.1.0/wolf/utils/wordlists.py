"""
Wordlist management for Wolf toolkit
"""

import os

def get_subdomain_wordlist():
    """
    Get default subdomain wordlist
    
    Returns:
        list: Default subdomain wordlist
    """
    return [
        'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
        'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'test', 'dev', 'staging',
        'admin', 'api', 'blog', 'forum', 'shop', 'store', 'mobile', 'm', 'wap',
        'secure', 'vpn', 'remote', 'mx', 'mx1', 'mx2', 'imap', 'pop3', 'exchange',
        'webdav', 'cms', 'portal', 'intranet', 'extranet', 'support', 'help', 'docs',
        'wiki', 'kb', 'news', 'media', 'images', 'img', 'static', 'assets', 'cdn',
        'downloads', 'files', 'upload', 'uploads', 'backup', 'old', 'new', 'demo',
        'beta', 'alpha', 'rc', 'release', 'preview', 'sandbox', 'lab', 'labs',
        'research', 'internal', 'private', 'public', 'guest', 'user', 'users',
        'member', 'members', 'client', 'clients', 'customer', 'customers', 'partner',
        'partners', 'vendor', 'vendors', 'supplier', 'suppliers', 'affiliate',
        'affiliates', 'reseller', 'resellers', 'dealer', 'dealers', 'distributor',
        'distributors', 'subdomain', 'sub', 'gateway', 'router', 'switch', 'firewall',
        'proxy', 'cache', 'load', 'balance', 'cluster', 'node', 'server', 'host',
        'service', 'app', 'application', 'web', 'site', 'website', 'domain', 'zone',
        'dns', 'ntp', 'time', 'sync', 'backup', 'mirror', 'replica', 'slave',
        'master', 'primary', 'secondary', 'tertiary', 'prod', 'production', 'live',
        'staging', 'qa', 'quality', 'assurance', 'testing', 'test', 'dev', 'development',
        'local', 'localhost', 'internal', 'external', 'dmz', 'lan', 'wan', 'vpn',
        'ssl', 'tls', 'https', 'secure', 'auth', 'login', 'signin', 'signup',
        'register', 'registration', 'account', 'profile', 'dashboard', 'panel',
        'control', 'manage', 'management', 'console', 'shell', 'terminal', 'ssh',
        'telnet', 'rdp', 'vnc', 'remote', 'desktop', 'citrix', 'vmware', 'hyper',
        'xen', 'kvm', 'docker', 'container', 'kubernetes', 'k8s', 'openshift'
    ]

def get_directory_wordlist():
    """
    Get default directory wordlist
    
    Returns:
        list: Default directory wordlist
    """
    return [
        'admin', 'administrator', 'test', 'backup', 'old', 'new', 'temp', 'tmp',
        'cache', 'logs', 'log', 'config', 'conf', 'configuration', 'settings',
        'setup', 'install', 'installation', 'upgrade', 'update', 'patch', 'patches',
        'data', 'database', 'db', 'sql', 'mysql', 'postgres', 'oracle', 'mssql',
        'sqlite', 'mongodb', 'redis', 'memcache', 'files', 'file', 'uploads',
        'upload', 'download', 'downloads', 'docs', 'documents', 'documentation',
        'manual', 'help', 'support', 'faq', 'readme', 'changelog', 'license',
        'legal', 'privacy', 'terms', 'tos', 'policy', 'policies', 'about',
        'contact', 'info', 'information', 'news', 'blog', 'forum', 'community',
        'social', 'share', 'sharing', 'media', 'images', 'img', 'picture',
        'pictures', 'photo', 'photos', 'gallery', 'galleries', 'video', 'videos',
        'audio', 'music', 'sound', 'sounds', 'css', 'js', 'javascript', 'style',
        'styles', 'stylesheet', 'stylesheets', 'script', 'scripts', 'lib', 'libs',
        'library', 'libraries', 'framework', 'frameworks', 'plugin', 'plugins',
        'module', 'modules', 'component', 'components', 'widget', 'widgets',
        'theme', 'themes', 'template', 'templates', 'layout', 'layouts', 'page',
        'pages', 'view', 'views', 'partial', 'partials', 'include', 'includes',
        'common', 'shared', 'public', 'private', 'protected', 'secure', 'security',
        'auth', 'authentication', 'authorization', 'login', 'logout', 'signin',
        'signout', 'signup', 'register', 'registration', 'account', 'profile',
        'user', 'users', 'member', 'members', 'client', 'clients', 'customer',
        'customers', 'guest', 'guests', 'visitor', 'visitors', 'session', 'sessions',
        'cookie', 'cookies', 'token', 'tokens', 'key', 'keys', 'secret', 'secrets',
        'password', 'passwords', 'hash', 'hashes', 'salt', 'salts', 'encryption',
        'decrypt', 'decryption', 'encode', 'decode', 'base64', 'md5', 'sha1',
        'sha256', 'sha512', 'api', 'rest', 'soap', 'xml', 'json', 'ajax',
        'service', 'services', 'web', 'webservice', 'webservices', 'endpoint',
        'endpoints', 'resource', 'resources', 'controller', 'controllers', 'action',
        'actions', 'method', 'methods', 'function', 'functions', 'procedure',
        'procedures', 'query', 'queries', 'search', 'find', 'filter', 'sort',
        'order', 'group', 'join', 'select', 'insert', 'update', 'delete',
        'create', 'read', 'write', 'execute', 'run', 'start', 'stop', 'restart',
        'reload', 'refresh', 'reset', 'clear', 'clean', 'purge', 'flush',
        'sync', 'synchronize', 'export', 'import', 'migrate', 'migration',
        'migrations', 'seed', 'seeder', 'seeders', 'fixture', 'fixtures',
        'sample', 'samples', 'example', 'examples', 'demo', 'demos', 'tutorial',
        'tutorials', 'guide', 'guides', 'howto', 'walkthrough', 'step', 'steps'
    ]

def load_wordlist_from_file(file_path):
    """
    Load wordlist from file
    
    Args:
        file_path (str): Path to wordlist file
        
    Returns:
        list: Wordlist entries or empty list if file not found
    """
    try:
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            wordlist = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    wordlist.append(line)
            return wordlist
            
    except Exception:
        return []

def save_wordlist_to_file(wordlist, file_path):
    """
    Save wordlist to file
    
    Args:
        wordlist (list): Wordlist to save
        file_path (str): Output file path
        
    Returns:
        bool: True if successful
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            for word in wordlist:
                f.write(f"{word}\n")
        return True
    except Exception:
        return False

def merge_wordlists(*wordlists):
    """
    Merge multiple wordlists and remove duplicates
    
    Args:
        *wordlists: Variable number of wordlist arguments
        
    Returns:
        list: Merged wordlist without duplicates
    """
    merged = set()
    for wordlist in wordlists:
        if isinstance(wordlist, list):
            merged.update(wordlist)
        elif isinstance(wordlist, str) and os.path.exists(wordlist):
            file_wordlist = load_wordlist_from_file(wordlist)
            merged.update(file_wordlist)
    
    return sorted(list(merged))

def filter_wordlist(wordlist, min_length=1, max_length=None, exclude_patterns=None):
    """
    Filter wordlist based on criteria
    
    Args:
        wordlist (list): Wordlist to filter
        min_length (int): Minimum word length
        max_length (int): Maximum word length
        exclude_patterns (list): Patterns to exclude
        
    Returns:
        list: Filtered wordlist
    """
    import re
    
    filtered = []
    exclude_regex = None
    
    if exclude_patterns:
        exclude_regex = re.compile('|'.join(exclude_patterns), re.IGNORECASE)
    
    for word in wordlist:
        # Check length
        if len(word) < min_length:
            continue
        if max_length and len(word) > max_length:
            continue
        
        # Check exclude patterns
        if exclude_regex and exclude_regex.search(word):
            continue
        
        filtered.append(word)
    
    return filtered
