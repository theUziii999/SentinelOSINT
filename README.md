OSINT-CLI
Framework OSINT da linea di comando per investigatori digitali, analisti di sicurezza e penetration tester.

✨ Caratteristiche principali
Recon dominio (DNS, WHOIS, SSL, subdomain scan)

Recon web (headers, fingerprinting, tecnologie)

Recon email (MX, breach check, validazione)

Report HTML/PDF

CLI moderna e modulare

Struttura estendibile con nuovi moduli

📦 Installazione
Codice
git clone https://github.com/theUziii999/osint-cli
cd osint-cli
pip install -r requirements.txt
🖥️ Utilizzo
Codice
python main.py domain example.com
python main.py email target@mail.com
python main.py web https://example.com
📁 Struttura del progetto
Codice
osint-cli/
├── main.py
├── modules/
│   ├── domain.py
│   ├── email.py
│   ├── web.py
├── utils/
│   ├── report.py
│   ├── logger.py
│   ├── helpers.py
├── requirements.txt
└── README.md
🧩 Moduli OSINT
Domain Recon → DNS, WHOIS, SSL, subdomain enumeration

Web Recon → headers, fingerprinting, tecnologie

Email Recon → validazione, MX, breach check

Report Engine → esportazione HTML/PDF

🛠️ Roadmap
Aggiunta API OSINT esterne

Dashboard web

Export JSON

Plugin system

Modalità automatizzata “full scan”

📄 Licenza
MIT License
