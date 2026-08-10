# DynDNS-Updater - Umsetzungsplan

## Phase 0 - Vorbereitung
- [ ] Cloudflare API-Token neu anlegen (Template "Edit zone DNS")
- [ ] Cloudflare Zone ID kopieren
- [ ] Subdomain-Liste erfassen
- [ ] FritzBox TR-064-User anlegen und testen
- [ ] Healthchecks-Check anlegen (15 Min Periode)

## Phase 1 - Repo
- [x] GitHub-Repo angelegt
- [x] Struktur + SPEC/PLAN committet

## Phase 2 - Kernmodule
- [x] config.py, state.py, fritzbox.py, cloudflare.py, freedns.py, healthcheck.py, main.py
- [x] notify.py (E-Mail-Notification bei IP-Aenderung)

## Phase 3 - Lokaler Test
- [ ] .env lokal befuellen (nicht committen)
- [ ] TR-064 gegen echte FritzBox testen
- [ ] Cloudflare-Update mit Test-Subdomain verifizieren
- [ ] FreeDNS-Call verifizieren
- [ ] Fehlerfaelle simulieren
- [ ] Webhook manuell triggern
- [ ] Idempotenz pruefen

## Phase 4 - Containerisierung
- [x] Dockerfile, docker-compose.yml
- [ ] docker build/run lokal testen
- [ ] Vollen Zyklus im Container testen

## Phase 5 - CI/Registry
- [x] build-and-push.yml
- [ ] GHCR-Sichtbarkeit pruefen
- [ ] Ersten Push/Actions-Lauf pruefen
- [ ] Tag v0.1.0

## Phase 6 - Deployment
- [ ] Zielverzeichnis auf Docker-Host anlegen
- [ ] compose + .env kopieren, docker login, up -d
- [ ] Logs und Healthcheck-Ping pruefen

## Phase 7 - FritzBox-Integration
- [ ] Custom-DynDNS-URL konfigurieren
- [ ] Webhook testen
- [ ] FreeDNS-Parallelbetrieb bestaetigen

## Phase 8 - Umstellung bestehender Subdomains
- [ ] Pro Subdomain einzeln: CNAME loeschen, A-Record (DNS-only) anlegen
- [ ] Erreichbarkeit von aussen pruefen
- [ ] Nicht-Standard-Port-Subdomains einzeln gegenchecken
- [ ] CLOUDFLARE_RECORDS final anpassen

## Phase 9 - Monitoring & Abnahme
- [ ] Watchtower-Lauf pruefen
- [ ] Healthchecks-Alarmierung testen
- [ ] Eine Woche Beobachtung
- [ ] Doku aktualisieren

## Phase 10 - Abschluss
- [ ] FreeDNS optional deaktivieren
- [ ] Proxy-Mode-Entscheidung erneut bewerten
- [ ] Redundanz pruefen
