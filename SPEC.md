# DynDNS-Updater - Spezifikation

**Status:** Entwurf fuer Umsetzung
**Zielumgebung:** Docker-Host (Debian VM auf Proxmox)
**Hosting:** GitHub (Repo + GitHub Actions)
**IP-Version:** Nur IPv4 (kein AAAA/IPv6 in v1)

## 1. Ziel

Abloesung des aktuellen Setups (Cloudflare-CNAME -> FreeDNS-Subdomain) durch einen selbst
gehosteten Updater-Container, der eine variable Anzahl Cloudflare-A-Records DNS-only (graue
Cloud) direkt mit der aktuellen oeffentlichen IPv4-Adresse pflegt und parallel weiterhin die
bestehende FreeDNS-Update-URL aufruft.

Trigger fuer einen Update-Zyklus:
1. Container-Start (Initial-Check)
2. Webhook-Aufruf (GET) von der FritzBox bei IP-Wechsel
3. Fallback-Polling alle 15 Minuten

Die tatsaechliche IP wird niemals aus Webhook-Parametern uebernommen. Der Container ermittelt
die IP bei jedem Trigger selbst ueber die FritzBox TR-064-Schnittstelle.

## 2. Ablauflogik

1. IP_aktuell = fritzbox.get_external_ip(retries=3, backoff=[2s,5s,10s])
2. IP_letzte = state.load()
3. Wenn gleich: Poll -> nur Heartbeat-Ping, kein Update. Webhook/Start -> nur Log.
4. Wenn unterschiedlich: Cloudflare-Records updaten, FreeDNS aufrufen, state speichern,
   Healthcheck-Erfolgs-Ping. Bei Teilfehler: state NICHT speichern, Fail-Ping.

## 3. Cloudflare

- Nur A-Records, DNS-only (proxied=false)
- Subdomain-Teile ueber CLOUDFLARE_RECORDS (ENV), relativ zur Zone (z.B. "sub1" oder "*.home", kein FQDN)
- Records pro Lauf per Name aufgeloest, nicht gecacht
- Benoetigter Token-Scope: Zone -> DNS -> Edit (Template "Edit zone DNS") + Zone -> Zone -> Read

## 4. Webhook

- GET /webhook/update, kein Auth, nur fuer internen LAN-Aufruf gedacht

## 5. Sicherheit

- .env niemals committen
- Cloudflare-Token nur mit minimal noetigen Rechten
- FritzBox-TR-064-User mit eingeschraenkten Rechten
- Alle Records bleiben DNS-only (kein Proxy-Mode in v1)

## 6. Offene Punkte

- IPv6/AAAA
- Proxy-Mode fuer reine HTTP(S)-Subdomains
- Redundanter Lauf auf zweitem Host
- Spaetere Abschaltung der FreeDNS-Anbindung
