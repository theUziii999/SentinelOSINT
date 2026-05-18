# SentinelOSINT

> Framework OSINT modulare da linea di comando per investigatori digitali, analisti di sicurezza e penetration tester. Recon rapido, report automatici, architettura estendibile.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-teal?style=flat-square)

---

## Indice

- [Caratteristiche](#caratteristiche)
- [Installazione](#installazione)
- [Utilizzo](#utilizzo)
- [Moduli OSINT](#moduli-osint)
- [Struttura del progetto](#struttura-del-progetto)
- [Roadmap](#roadmap)
- [Licenza](#licenza)

---

## Caratteristiche

- **Domain Recon** — DNS, WHOIS, SSL, subdomain enumeration
- **Web Recon** — HTTP headers, fingerprinting, rilevamento tecnologie
- **Email Recon** — validazione, MX lookup, breach check
- **Report Engine** — esportazione HTML e PDF con layout professionale
- **CLI moderna e modulare** — interfaccia chiara, output colorato
- **Architettura estendibile** — aggiungi nuovi moduli senza toccare il core

---

## Installazione

```bash
# 1. Clona il repository
git clone https://github.com/theUziii999/SentinelOSINT

# 2. Entra nella directory
cd SentinelOSINT

# 3. Installa le dipendenze
pip install -r requirements.txt
```

> **Requisiti:** Python 3.10 o superiore

---

## Utilizzo

```bash
# Domain reconnaissance
python main.py domain example.com

# Email investigation
python main.py email target@mail.com

# Web fingerprinting
python main.py web https://example.com
```

---

## Moduli OSINT

### Domain Recon — `modules/domain.py`

Analisi completa del dominio target:

- Enumerazione record DNS (A, MX, NS, TXT, CNAME)
- WHOIS lookup con parsing dei dati registrar
- Ispezione certificato SSL (scadenza, emittente, SAN)
- Subdomain enumeration tramite wordlist e bruteforce

### Web Recon — `modules/web.py`

Fingerprinting dell'infrastruttura web:

- Analisi degli HTTP response headers
- Rilevamento CMS, framework e librerie
- Controllo security headers (CSP, HSTS, X-Frame-Options...)
- Stack tecnologico (server, linguaggio, CDN)

### Email Recon — `modules/email.py`

Investigazione su indirizzi email:

- Validazione formato e sintassi RFC
- MX record lookup e verifica deliverability
- Breach check su database pubblici
- Stima del deliverability score

### Report Engine — `utils/report.py`

Esportazione automatica dei risultati:

- Export **HTML** con layout responsive e professionale
- Export **PDF** pronto per la documentazione
- Timestamp automatico su ogni report
- Intestazione con metadata della sessione di recon

---

## Struttura del progetto

```
SentinelOSINT/
├── main.py                  ← entry point CLI
├── modules/
│   ├── domain.py            ← DNS, WHOIS, SSL, subdomain
│   ├── email.py             ← MX, breach check, validazione
│   └── web.py               ← headers, fingerprinting, stack
├── utils/
│   ├── report.py            ← export HTML / PDF
│   ├── logger.py            ← logging centralizzato
│   └── helpers.py           ← funzioni condivise
├── requirements.txt
└── README.md
```

---

## Roadmap

| Stato | Feature |
|-------|---------|
| ✅ Done | Moduli domain, email, web |
| ✅ Done | Report engine HTML / PDF |
| 🔄 WIP | Integrazione API OSINT esterne (Shodan, VirusTotal, HaveIBeenPwned) |
| 📋 Planned | Export JSON |
| 📋 Planned | Plugin system estendibile |
| 📋 Planned | Modalità automatizzata "full scan" multi-target |
| 📋 Planned | Dashboard web con visualizzazione grafica dei risultati |

---

## Contribuire

Pull request e issue sono benvenute. Per modifiche rilevanti, apri prima una issue per discutere cosa vorresti cambiare.

1. Forka il repository
2. Crea un branch (`git checkout -b feature/nuova-funzione`)
3. Committa le modifiche (`git commit -m 'Aggiunge nuova funzione'`)
4. Pusha il branch (`git push origin feature/nuova-funzione`)
5. Apri una Pull Request

---

## Licenza

Distribuito sotto licenza **MIT**. Vedi il file `LICENSE` per i dettagli.

---

> ⚠️ **Disclaimer:** SentinelOSINT è pensato esclusivamente per attività di sicurezza autorizzate, ricerca e scopi educativi. L'utilizzo su sistemi senza esplicita autorizzazione è illegale e contrario all'etica della sicurezza informatica. L'autore declina ogni responsabilità per usi impropri.
