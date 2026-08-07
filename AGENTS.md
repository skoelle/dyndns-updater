# AGENTS.md

## Projekt

Kleiner Docker-Container, der Cloudflare-A-Records (DNS-only) + eine FreeDNS-URL mit der
aktuellen öffentlichen IPv4-Adresse pflegt. IP wird ausschließlich über die FritzBox
TR-064-Schnittstelle ermittelt.

Kontext: [`SPEC.md`](SPEC.md) (Design), [`PLAN.md`](PLAN.md) (Tasks),
[`README.md`](README.md) (Betrieb).

## Struktur

- `app/` – Kernmodule (Python 3.12)
  - `config.py` – ENV-basierte Konfiguration + Validierung
  - `state.py` – persistierte letzte IP (`/app/data/last-known-ip.json`, ephemeral im Container)
  - `fritzbox.py` – IP-Ermittlung via TR-064 (Retry/Backoff)
  - `cloudflare.py` – A-Record-Update (DNS-only)
  - `freedns.py` – FreeDNS-Update-Call
  - `healthcheck.py` – Healthchecks-Pings
  - `main.py` – Flask-Webhook (`/webhook/update`, `/healthz`) + Poll-Scheduler
- `.env.example` – Referenz aller ENV-Variablen (Pflicht: FRITZBOX_*, CLOUDFLARE_*)

## Befehle

- Tests: keine Test-Suite vorhanden
- Lint/Format: `ruff check .` und `ruff format --check .` (in `.venv` via
  `python3 -m venv .venv && . .venv/bin/activate`)
- Lokal: `python -m app.main` (im `.venv`, deps aus `requirements.txt`)
- Container: `docker compose up -d`

## Konventionen

- CREDENTIALS NIE committen. `.env` ist gitignored – nie mit `-f` hinzufügen.
- Keine Co-Autoren in Commits.
- Keine Kommentare im Code außer auf Nachfrage.
- Python-Code mit Ruff formatieren (line-length 100, double quotes).
- Änderungen an `SPEC.md`/`PLAN.md`/`README.md` mitziehen, wenn sich Design/Betrieb ändert.

## License

MIT License - Copyright (c) 2026 Stefan Koelle (https://stefankoelle.de)
- Full text in `LICENSE`
- License headers in all source code files
