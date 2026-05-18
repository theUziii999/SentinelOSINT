#!/usr/bin/env python3
"""
OSINT CLI Framework v1.0
Tool di raccolta informazioni per cybersecurity
Compatibile con Kali Linux e Windows
"""

import argparse
import sys
import os

# Aggiungi la cartella corrente al path per i moduli
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from colorama import init, Fore, Style
from utils.config import Colors
from utils.helpers import print_banner, is_valid_domain, is_valid_email
from modules.domain_recon import DomainRecon
from modules.web_recon import WebRecon
from modules.email_osint import EmailOSINT
from modules.report_generator import ReportGenerator

# Inizializza colorama per Windows
init(autoreset=True)


def show_banner():
    """
    Mostra il banner iniziale del tool
    """
    banner_text = f"""
{Fore.CYAN}   ____   _____ _____ _   _ _______ 
  / __ \\ / ____|_   _| \\ | |__   __|
 | |  | | (___   | | |  \\| |  | |   
 | |  | |\\___ \\  | | | . ` |  | |   
 | |__| |____) |_| |_| |\\  |  | |   
  \\____/|_____/|_____|_| \\_|  |_|   {Style.RESET_ALL}
  
{Fore.GREEN}    OSINT Framework CLI v1.0{Style.RESET_ALL}
{Fore.YELLOW}    For Educational & Authorized Testing Only{Style.RESET_ALL}
    """
    print(banner_text)


def run_domain_recon(domain, verbose=False):
    """
    Esegue la ricognizione di dominio
    """
    if verbose:
        print(f"{Fore.YELLOW}[*] Avvio ricognizione dominio: {domain}{Style.RESET_ALL}")
    
    try:
        recon = DomainRecon(domain)
        results = recon.run_all()
        
        if verbose:
            print(f"{Fore.GREEN}[+] Ricognizione dominio completata{Style.RESET_ALL}")
            print(f"    - WHOIS: {len(results['whois'])} campi raccolti")
            print(f"    - DNS Records: {len(results['dns'])} tipi")
            print(f"    - Subdomains trovati: {len(results['subdomains'])}")
            print(f"    - IP Info: {'OK' if 'resolved_ip' in results['ip_info'] else 'Errore'}")
        
        return results
    
    except Exception as e:
        print(f"{Fore.RED}[!] Errore nella ricognizione dominio: {str(e)}{Style.RESET_ALL}")
        return {'error': str(e)}


def run_web_recon(url, verbose=False):
    """
    Esegue la ricognizione web
    """
    if verbose:
        print(f"{Fore.YELLOW}[*] Avvio ricognizione web: {url}{Style.RESET_ALL}")
    
    try:
        recon = WebRecon(url)
        results = recon.run_all()
        
        if verbose:
            print(f"{Fore.GREEN}[+] Ricognizione web completata{Style.RESET_ALL}")
            print(f"    - Status Code: {results.get('status_code', 'N/A')}")
            print(f"    - Tecnologie rilevate: {len(results['technologies'])}")
            print(f"    - File discovery: {len(results['discovery'])}")
        
        return results
    
    except Exception as e:
        print(f"{Fore.RED}[!] Errore nella ricognizione web: {str(e)}{Style.RESET_ALL}")
        return {'error': str(e)}


def run_email_osint(email, verbose=False):
    """
    Esegue l'OSINT su email
    """
    if verbose:
        print(f"{Fore.YELLOW}[*] Avvio OSINT email: {email}{Style.RESET_ALL}")
    
    try:
        recon = EmailOSINT(email)
        results = recon.run_all()
        
        if verbose:
            print(f"{Fore.GREEN}[+] OSINT email completato{Style.RESET_ALL}")
            print(f"    - Formato valido: {'Sì' if results['valid_format'] else 'No'}")
            print(f"    - Dominio: {results.get('domain', 'N/A')}")
            print(f"    - Email temporanea: {'Sì' if results['disposable'] else 'No'}")
        
        return results
    
    except Exception as e:
        print(f"{Fore.RED}[!] Errore nell'OSINT email: {str(e)}{Style.RESET_ALL}")
        return {'error': str(e)}


def generate_reports(data, target, output_format, verbose=False):
    """
    Genera i report nei formati richiesti
    """
    if verbose:
        print(f"{Fore.YELLOW}[*] Generazione report in formato: {output_format}{Style.RESET_ALL}")
    
    try:
        generator = ReportGenerator(data, target)
        generated_files = []
        
        if output_format in ['json', 'all']:
            filepath = generator.to_json()
            generated_files.append(filepath)
            if verbose:
                print(f"{Fore.CYAN}    [JSON] {filepath}{Style.RESET_ALL}")
        
        if output_format in ['txt', 'all']:
            filepath = generator.to_txt()
            generated_files.append(filepath)
            if verbose:
                print(f"{Fore.CYAN}    [TXT]  {filepath}{Style.RESET_ALL}")
        
        if output_format in ['pdf', 'all']:
            filepath = generator.to_pdf()
            generated_files.append(filepath)
            if verbose:
                print(f"{Fore.CYAN}    [PDF]  {filepath}{Style.RESET_ALL}")
        
        if verbose:
            print(f"{Fore.GREEN}[+] Report generati con successo: {len(generated_files)} file{Style.RESET_ALL}")
        
        return generated_files
    
    except Exception as e:
        print(f"{Fore.RED}[!] Errore nella generazione report: {str(e)}{Style.RESET_ALL}")
        return []


def validate_inputs(args):
    """
    Valida gli input dell'utente
    """
    errors = []
    
    if args.domain and not is_valid_domain(args.domain):
        errors.append(f"Dominio non valido: {args.domain}")
    
    if args.email and not is_valid_email(args.email):
        errors.append(f"Email non valida: {args.email}")
    
    if not any([args.domain, args.url, args.email]):
        errors.append("Nessun target specificato. Usa -d, -u o -e")
    
    return errors


def main():
    """
    Funzione principale - gestisce gli argomenti CLI
    """
    # Parser degli argomenti
    parser = argparse.ArgumentParser(
        description='OSINT Framework CLI - Raccolta informazioni per cybersecurity',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.CYAN}Esempi d'uso:{Style.RESET_ALL}
  python main.py -d example.com                    # Solo dominio
  python main.py -d example.com -o all             # Dominio + tutti i report
  python main.py -u https://example.com            # Solo web
  python main.py -e admin@example.com              # Solo email
  python main.py -d example.com -e admin@example.com -o pdf  # Combinato + PDF
  python main.py -d example.com -v                 # Modalità verbose
        """
    )
    
    # Argomenti
    parser.add_argument(
        '-d', '--domain',
        help='Target dominio (es: example.com)',
        type=str
    )
    
    parser.add_argument(
        '-u', '--url',
        help='Target URL (es: https://example.com)',
        type=str
    )
    
    parser.add_argument(
        '-e', '--email',
        help='Target email (es: admin@example.com)',
        type=str
    )
    
    parser.add_argument(
        '-o', '--output',
        choices=['json', 'txt', 'pdf', 'all'],
        default='json',
        help='Formato output report (default: json)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Modalità verbose - mostra dettagli operazioni'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Nasconde il banner iniziale'
    )
    
    # Parsing
    args = parser.parse_args()
    
    # Mostra banner
    if not args.no_banner:
        show_banner()
    
    # Validazione input
    errors = validate_inputs(args)
    if errors:
        print(f"{Fore.RED}[!] Errori di validazione:{Style.RESET_ALL}")
        for error in errors:
            print(f"    - {error}")
        parser.print_help()
        sys.exit(1)
    
    # Raccolta dati
    all_results = {}
    target_name = args.domain or args.url or args.email
    
    if args.verbose:
        print_banner(f"INIZIO RICERCA: {target_name}", char="=")
    
    # Domain Recon
    if args.domain:
        all_results['domain_recon'] = run_domain_recon(args.domain, args.verbose)
    
    # Web Recon
    if args.url or args.domain:
        target_url = args.url or args.domain
        all_results['web_recon'] = run_web_recon(target_url, args.verbose)
    
    # Email OSINT
    if args.email:
        all_results['email_osint'] = run_email_osint(args.email, args.verbose)
    
    # Generazione report
    if args.verbose:
        print_banner("GENERAZIONE REPORT", char="=")
    
    generated = generate_reports(all_results, target_name, args.output, args.verbose)
    
    # Riepilogo finale
    if not args.no_banner:
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}RICERCA COMPLETATA{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"Target: {target_name}")
        print(f"Moduli eseguiti: {len(all_results)}")
        print(f"Report generati: {len(generated)}")
        for f in generated:
            print(f"  - {f}")
        print(f"\n{Fore.YELLOW}Ricorda: usa questo tool solo su target autorizzati!{Style.RESET_ALL}")
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Interrotto dall'utente{Style.RESET_ALL}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Errore critico: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)