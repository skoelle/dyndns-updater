# 🌐 dyndns-updater

Kleiner Docker-Container, der Cloudflare-A-Records (DNS-only) und eine bestehende
FreeDNS-Update-URL mit der aktuellen öffentlichen IPv4-Adresse aktuell hält.

Details siehe [SPEC.md](SPEC.md) (Architektur/Design) und [PLAN.md](PLAN.md)
(Umsetzungs-Tasks).

## 📋 Kurzüberblick

- 🏠 IP wird ausschließlich über die FritzBox TR-064-Schnittstelle ermittelt (nicht aus
  Webhook-Parametern übernommen)
- ⏰ Trigger: Container-Start, `GET /webhook/update` (kein Auth, rein intern),
  Fallback-Polling alle 15 Minuten
- 🔄 DNS-Update (Cloudflare + FreeDNS) nur bei tatsächlicher IP-Änderung
- 💚 Healthcheck-Heartbeat bei jedem Poll-Zyklus, unabhängig von einer IP-Änderung

## 🚀 Quickstart

```bash
cp .env.example .env
vim .env   # Werte eintragen
docker compose up -d
```

## ⚙️ Konfiguration (`.env`)

Alle Einstellungen erfolgen ausschließlich über Umgebungsvariablen (siehe
[`.env.example`](.env.example)). Pflichtfelder:

| Variable | Zweck |
| --- | --- |
| `FRITZBOX_HOST`, `_USER`, `_PASSWORD` | 🏠 TR-064-Zugang zur FritzBox (IP-Quelle) |
| `CLOUDFLARE_API_TOKEN` | ☁️ Cloudflare-Token (Zone -> DNS -> Edit) |
| `CLOUDFLARE_ZONE_ID` | ☁️ Cloudflare-Zone |
| `CLOUDFLARE_RECORDS` | 📝 Kommagetrennte A-Record-Namen (DNS-only) |

Optional: `FREEDNS_UPDATE_URL`, `POLL_INTERVAL_MINUTES`,
`HEALTHCHECK_PING_URL`, `TZ`, `LOG_LEVEL`. Die IP kommt ausschließlich aus der
FritzBox, nie aus Webhook-Parametern.

### 📧 E-Mail-Notification (optional)

Bei IP-Änderung wird eine HTML-E-Mail mit Emojis versendet, wenn SMTP-Konfiguration
vorliegt:

| Variable | Zweck |
| --- | --- |
| `SMTP_HOST` | 📮 SMTP-Server (z.B. `smtp.gmail.com`) |
| `SMTP_PORT` | 🚪 Port (Default: `587`) |
| `SMTP_USER` | 👤 SMTP-Login |
| `SMTP_PASSWORD` | 🔒 SMTP-Passwort |
| `NOTIFY_EMAIL_TO` | 📬 Empfänger-Adresse |
| `NOTIFY_EMAIL_FROM` | 📤 Absender-Adresse |

## 🔧 Betrieb

- **💾 State (bewusst ohne Volume, ephemeral):** zuletzt bekannte IP liegt als
  `data/last-known-ip.json` im Container. Bei jedem neu erstellten Container ist
  der State wieder leer, wodurch beim Start ein Force-Push erzwungen wird.
  Die Änderung wird erst nach erfolgreichem Update gespeichert.
- **🪝 Webhook:** `GET /webhook/update` (kein Auth, intern, Port fest 8090) löst einen Zyklus aus.
- **💓 Healthz:** `GET /healthz` für den Container-Healthcheck (genutzt vom Docker-`HEALTHCHECK`).
- **🏥 Healthchecks:** Healthy Ping bei jedem Poll, Failure Ping bei IP-Fehler bzw. Teilfehler.
- **📊 Logs/Wartung:** `docker compose logs -f`; Updates via Watchtower (Label im Compose).

## 🧪 Test/Quality

```bash
python3 -m venv .venv && . .venv/bin/activate   # virtuelles Umfeld
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
ruff format --check .
```

## 🏗️ Build

Wird automatisch per GitHub Actions nach `ghcr.io/skoelle/dyndns-updater` gebaut
(siehe `.github/workflows/build-and-push.yml`).

## 📄 License

Licensed under the [MIT License](LICENSE) - Copyright (c) 2026 Stefan Koelle (https://stefankoelle.de)
