"""
Configurazione base del progetto OSINT CLI
"""

import os

# API Keys - usa variabili d'ambiente per sicurezza
# Esempio: export SHODAN_API_KEY="tua-chiave" su Linux/Mac
#          set SHODAN_API_KEY=tua-chiave su Windows CMD
SHODAN_API_KEY = os.getenv("SHODAN_API_KEY", "")
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY", "")

# Impostazioni generali
TIMEOUT = 10  # secondi per le richieste HTTP
USER_AGENT = "OSINT-CLI-Tool/1.0 (Educational Purpose)"

# Percorsi
WORDLIST_PATH = "data/wordlists/subdomains.txt"
REPORTS_DIR = "reports"

# Colori per il terminale (usato con colorama)
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"