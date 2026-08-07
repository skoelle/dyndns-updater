# dyndns-updater

Kleiner Docker-Container, der Cloudflare-A-Records (DNS-only) und eine bestehende
FreeDNS-Update-URL mit der aktuellen öffentlichen IPv4-Adresse aktuell hält.

Details siehe [SPEC.md](SPEC.md) (Architektur/Design) und [PLAN.md](PLAN.md)
(Umsetzungs-Tasks).

## Kurzüberblick

- IP wird ausschließlich über die FritzBox TR-064-Schnittstelle ermittelt (nicht aus
  Webhook-Parametern übernommen)
- Trigger: Container-Start, `GET /webhook/update` (kein Auth, rein intern),
  Fallback-Polling alle 15 Minuten
- DNS-Update (Cloudflare + FreeDNS) nur bei tatsächlicher IP-Änderung
- Healthcheck-Heartbeat bei jedem Poll-Zyklus, unabhängig von einer IP-Änderung

## Quickstart

```bash
cp .env.example .env
vim .env   # Werte eintragen (CLOUDFLARE_RECORDS: nur Subdomain-Teile, z.B. "sub1,sub2,*.home")
docker compose up -d
```

## Build

Wird automatisch per GitHub Actions nach `ghcr.io/skoelle/dyndns-updater` gebaut
(siehe `.github/workflows/build-and-push.yml`).
