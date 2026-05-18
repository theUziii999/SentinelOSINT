"""
Funzioni di utilità per il progetto OSINT CLI
"""

import re
import socket
from urllib.parse import urlparse


def is_valid_domain(domain):
    """
    Verifica se una stringa è un dominio valido.
    Esempio: example.com -> True
    """
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return bool(re.match(pattern, domain)) and '.' in domain


def is_valid_email(email):
    """
    Verifica se una stringa è una email valida.
    Esempio: test@example.com -> True
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_ip(ip):
    """
    Verifica se una stringa è un indirizzo IP valido (IPv4).
    Esempio: 192.168.1.1 -> True
    """
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def clean_url(url):
    """
    Pulisce e normalizza un URL.
    Aggiunge https:// se manca lo schema.
    Esempio: example.com -> https://example.com
    """
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url


def extract_domain_from_url(url):
    """
    Estrae il dominio da un URL.
    Esempio: https://www.example.com/path -> www.example.com
    """
    parsed = urlparse(clean_url(url))
    return parsed.netloc


def print_banner(text, char="="):
    """
    Stampa un banner decorativo nel terminale.
    """
    line = char * (len(text) + 4)
    print(f"\n{line}")
    print(f"{char} {text} {char}")
    print(f"{line}\n")


def truncate_string(text, max_length=100):
    """
    Tronca una stringa se troppo lunga, aggiungendo '...'.
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text