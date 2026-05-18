"""
Modulo per la ricognizione web
Analizza header, tecnologie, robots.txt, sitemap.xml
"""

import requests
from bs4 import BeautifulSoup
from utils.config import TIMEOUT, USER_AGENT
from utils.helpers import clean_url


class WebRecon:
    """
    Classe per la ricognizione di un sito web
    """
    
    def __init__(self, url):
        self.url = clean_url(url)
        self.results = {
            'target_url': self.url,
            'headers': {},
            'status_code': None,
            'technologies': [],
            'title': '',
            'meta_description': '',
            'discovery': {},
            'links': []
        }
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def get_headers(self):
        """
        Recupera gli header HTTP della risposta
        """
        try:
            resp = self.session.head(self.url, timeout=TIMEOUT, allow_redirects=True)
            self.results['status_code'] = resp.status_code
            self.results['headers'] = dict(resp.headers)
            
            # Se head fallisce, prova con GET
            if resp.status_code >= 400:
                resp = self.session.get(self.url, timeout=TIMEOUT)
                self.results['status_code'] = resp.status_code
                self.results['headers'] = dict(resp.headers)
                
        except requests.exceptions.Timeout:
            self.results['error'] = 'Timeout - il server non risponde'
        except requests.exceptions.ConnectionError:
            self.results['error'] = 'Errore di connessione - sito non raggiungibile'
        except Exception as e:
            self.results['error'] = str(e)
        
        return self
    
    def get_technologies(self):
        """
        Rileva le tecnologie usate dal sito analizzando header e HTML
        """
        tech = []
        headers = self.results.get('headers', {})
        
        # Analisi header
        server = headers.get('Server', '')
        if server:
            tech.append(f'Server: {server}')
        
        powered_by = headers.get('X-Powered-By', '')
        if powered_by:
            tech.append(f'Powered-By: {powered_by}')
        
        via = headers.get('Via', '')
        if via:
            tech.append(f'Proxy/Via: {via}')
        
        # Framework da header
        if 'cloudflare' in str(headers).lower():
            tech.append('Cloudflare CDN')
        if 'nginx' in server.lower():
            tech.append('Nginx Web Server')
        if 'apache' in server.lower():
            tech.append('Apache Web Server')
        if 'microsoft-iis' in server.lower():
            tech.append('Microsoft IIS')
        
        # Analisi HTML
        try:
            resp = self.session.get(self.url, timeout=TIMEOUT)
            html = resp.text.lower()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Titolo pagina
            title_tag = soup.find('title')
            if title_tag:
                self.results['title'] = title_tag.get_text(strip=True)
            
            # Meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                self.results['meta_description'] = meta_desc.get('content', '')
            
            # CMS detection
            if soup.find('meta', {'name': 'generator'}):
                cms = soup.find('meta', {'name': 'generator'})['content']
                tech.append(f'CMS: {cms}')
            
            # Framework JS detection
            if 'wp-content' in html or 'wp-includes' in html:
                tech.append('WordPress')
            if 'drupal' in html:
                tech.append('Drupal')
            if 'joomla' in html:
                tech.append('Joomla')
            if 'jquery' in html:
                tech.append('jQuery')
            if 'react' in html:
                tech.append('React')
            if 'vue' in html:
                tech.append('Vue.js')
            if 'angular' in html:
                tech.append('Angular')
            if 'bootstrap' in html:
                tech.append('Bootstrap')
            if 'laravel' in html:
                tech.append('Laravel')
            if 'django' in html:
                tech.append('Django')
            
            # Google Analytics / Tag Manager
            if 'google-analytics' in html or 'gtag' in html:
                tech.append('Google Analytics')
            if 'googletagmanager' in html:
                tech.append('Google Tag Manager')
            
            # E-commerce
            if 'shopify' in html:
                tech.append('Shopify')
            if 'woocommerce' in html:
                tech.append('WooCommerce')
            if 'magento' in html:
                tech.append('Magento')
            
        except Exception as e:
            tech.append(f'Errore analisi HTML: {str(e)}')
        
        self.results['technologies'] = tech
        return self
    
    def get_discovery_files(self):
        """
        Cerca file di discovery: robots.txt, sitemap.xml, security.txt
        """
        files_to_check = {
            'robots.txt': '/robots.txt',
            'sitemap.xml': '/sitemap.xml',
            'security.txt': '/.well-known/security.txt',
            'humans.txt': '/humans.txt'
        }
        
        for name, path in files_to_check.items():
            try:
                resp = self.session.get(
                    f"{self.url}{path}", 
                    timeout=TIMEOUT,
                    allow_redirects=False
                )
                if resp.status_code == 200:
                    # Limita a 2000 caratteri per non appesantire
                    content = resp.text[:2000]
                    self.results['discovery'][name] = {
                        'status': 200,
                        'content': content,
                        'size': len(resp.text)
                    }
                else:
                    self.results['discovery'][name] = {
                        'status': resp.status_code,
                        'found': False
                    }
            except:
                self.results['discovery'][name] = {
                    'status': 'error',
                    'found': False
                }
        
        return self
    
    def get_links(self):
        """
        Estrae i link interni dalla homepage
        """
        try:
            resp = self.session.get(self.url, timeout=TIMEOUT)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            links = set()
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Prendi solo link interni
                if href.startswith('/') or self.url in href:
                    links.add(href)
            
            self.results['links'] = list(links)[:20]  # Max 20 link
            
        except:
            self.results['links'] = []
        
        return self
    
    def run_all(self):
        """
        Esegue tutte le ricognizioni web in sequenza
        """
        self.get_headers()
        self.get_technologies()
        self.get_discovery_files()
        self.get_links()
        return self.results