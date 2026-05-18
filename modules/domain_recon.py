"""
Modulo per la ricognizione di dominio
Recupera WHOIS, DNS records, subdomains e info IP
"""

import whois
import dns.resolver
import requests
import socket
from utils.config import TIMEOUT, USER_AGENT


class DomainRecon:
    """
    Classe per la ricognizione completa di un dominio
    """
    
    def __init__(self, domain):
        self.domain = domain
        self.results = {
            'target': domain,
            'whois': {},
            'dns': {},
            'subdomains': [],
            'ip_info': {}
        }
    
    def get_whois(self):
        """
        Recupera informazioni WHOIS del dominio
        """
        try:
            w = whois.whois(self.domain)
            self.results['whois'] = {
                'registrar': w.registrar if w.registrar else 'N/A',
                'creation_date': str(w.creation_date) if w.creation_date else 'N/A',
                'expiration_date': str(w.expiration_date) if w.expiration_date else 'N/A',
                'name_servers': w.name_servers if w.name_servers else [],
                'emails': w.emails if w.emails else [],
                'org': w.org if w.org else 'N/A',
                'country': w.country if w.country else 'N/A'
            }
        except Exception as e:
            self.results['whois'] = {'error': str(e)}
        return self
    
    def get_dns_records(self):
        """
        Recupera i record DNS principali (A, AAAA, MX, NS, TXT, SOA)
        """
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(self.domain, record_type)
                self.results['dns'][record_type] = [str(rdata) for rdata in answers]
            except dns.resolver.NXDOMAIN:
                self.results['dns'][record_type] = ['Dominio non esistente']
            except dns.resolver.NoAnswer:
                self.results['dns'][record_type] = []
            except Exception as e:
                self.results['dns'][record_type] = [f'Errore: {str(e)}']
        
        return self
    
    def get_subdomains(self, wordlist=None):
        """
        Brute force dei subdomain con una wordlist
        Se non fornita, usa una lista di subdomain comuni
        """
        if not wordlist:
            wordlist = [
                'www', 'mail', 'ftp', 'admin', 'blog', 'shop', 
                'api', 'dev', 'test', 'staging', 'portal', 
                'webmail', 'remote', 'vpn', 'ns1', 'ns2'
            ]
        
        found = []
        
        for sub in wordlist:
            subdomain = f"{sub}.{self.domain}"
            try:
                dns.resolver.resolve(subdomain, 'A')
                found.append(subdomain)
            except:
                pass  # Subdomain non esistente
        
        self.results['subdomains'] = found
        return self
    
    def get_ip_info(self):
        """
        Recupera informazioni sull'IP principale del dominio
        Usa ipinfo.io API gratuita
        """
        try:
            # Risolvi l'IP del dominio
            ip = socket.gethostbyname(self.domain)
            self.results['ip_info']['resolved_ip'] = ip
            
            # Recupera info geografiche
            response = requests.get(
                f"https://ipinfo.io/{ip}/json",
                timeout=TIMEOUT,
                headers={'User-Agent': USER_AGENT}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.results['ip_info'].update({
                    'city': data.get('city', 'N/A'),
                    'region': data.get('region', 'N/A'),
                    'country': data.get('country', 'N/A'),
                    'org': data.get('org', 'N/A'),
                    'loc': data.get('loc', 'N/A'),  # latitudine,longitudine
                    'timezone': data.get('timezone', 'N/A')
                })
            else:
                self.results['ip_info']['error'] = f'Status code: {response.status_code}'
                
        except Exception as e:
            self.results['ip_info'] = {'error': str(e)}
        
        return self
    
    def run_all(self):
        """
        Esegue tutte le ricognizioni in sequenza
        """
        self.get_whois()
        self.get_dns_records()
        self.get_subdomains()
        self.get_ip_info()
        return self.results