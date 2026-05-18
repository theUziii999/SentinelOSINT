"""
Modulo per l'OSINT su indirizzi email
Verifica formato, controlla breach, analizza dominio
"""

import requests
import re
from utils.config import HUNTER_API_KEY, TIMEOUT, USER_AGENT


class EmailOSINT:
    """
    Classe per la ricognizione di un indirizzo email
    """
    
    def __init__(self, email):
        self.email = email.strip().lower()
        self.results = {
            'target_email': self.email,
            'valid_format': False,
            'domain': '',
            'breaches': [],
            'domain_info': {},
            'email_pattern': '',
            'disposable': False
        }
    
    def verify_format(self):
        """
        Verifica che l'email abbia un formato valido
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        self.results['valid_format'] = bool(re.match(pattern, self.email))
        
        if self.results['valid_format']:
            self.results['domain'] = self.email.split('@')[1]
        
        return self
    
    def check_disposable(self):
        """
        Verifica se l'email usa un provider di email temporanee/disposable
        """
        disposable_domains = [
            'tempmail.com', '10minutemail.com', 'guerrillamail.com',
            'mailinator.com', 'yopmail.com', 'throwawaymail.com',
            'temp-mail.org', 'fakeemail.com', 'sharklasers.com',
            'getairmail.com', 'burnermail.io'
        ]
        
        domain = self.results.get('domain', '')
        self.results['disposable'] = domain in disposable_domains
        
        return self
    
    def check_breach(self):
        """
        Controlla se l'email è stata coinvolta in data breach noti
        NOTA: HaveIBeenPwned richiede una API key a pagamento
        Questa è una simulazione/placeholder per l'implementazione reale
        """
        # Placeholder - per implementazione reale serve API key HIBP
        self.results['breaches'] = {
            'note': 'HaveIBeenPwned API richiede key a pagamento',
            'checked': False,
            'breaches_found': [],
            'source': 'https://haveibeenpwned.com/'
        }
        
        # Alternativa gratuita: verifica se il dominio è noto per breach
        try:
            # Usiamo un servizio alternativo gratuito come placeholder
            response = requests.get(
                f"https://emailrep.io/{self.email}",
                timeout=TIMEOUT,
                headers={'User-Agent': USER_AGENT, 'Key': ' gratuita limitata'}
            )
            if response.status_code == 200:
                data = response.json()
                self.results['breaches']['reputation'] = data.get('reputation', 'unknown')
                self.results['breaches']['suspicious'] = data.get('suspicious', False)
        except:
            pass
        
        return self
    
    def domain_enrichment(self):
        """
        Usa Hunter.io per trovare pattern email e info sul dominio
        NOTA: Richiede API key gratuita (100 req/mese)
        """
        if not HUNTER_API_KEY:
            self.results['domain_info'] = {
                'note': 'Hunter.io API key non configurata',
                'setup': 'export HUNTER_API_KEY=tua-chiave'
            }
            return self
        
        try:
            domain = self.results['domain']
            response = requests.get(
                f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}",
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                
                self.results['domain_info'] = {
                    'organization': data.get('organization', 'N/A'),
                    'domain': data.get('domain', domain),
                    'emails_found': len(data.get('emails', [])),
                    'pattern': data.get('pattern', 'N/A'),
                    'webmail': data.get('webmail', False)
                }
                
                # Salva il pattern email
                self.results['email_pattern'] = data.get('pattern', '')
            else:
                self.results['domain_info'] = {
                    'error': f'Status code: {response.status_code}'
                }
                
        except Exception as e:
            self.results['domain_info'] = {'error': str(e)}
        
        return self
    
    def verify_email_exists(self):
        """
        Verifica se l'email esiste realmente (SMTP verification)
        NOTA: Molti server bloccano questa verifica per privacy
        """
        # Placeholder - la verifica SMTP è complessa e spesso bloccata
        self.results['smtp_check'] = {
            'note': 'Verifica SMTP spesso bloccata dai server per privacy',
            'checked': False,
            'exists': 'unknown'
        }
        
        return self
    
    def run_all(self):
        """
        Esegue tutte le ricognizioni email in sequenza
        """
        self.verify_format()
        self.check_disposable()
        self.check_breach()
        self.domain_enrichment()
        self.verify_email_exists()
        return self.results