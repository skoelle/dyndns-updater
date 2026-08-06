import logging

import requests

log = logging.getLogger("freedns")


def update(update_url: str, timeout: int = 15) -> bool:
    if not update_url:
        log.info("Kein FREEDNS_UPDATE_URL konfiguriert - FreeDNS-Update wird ausgelassen.")
        return True
    try:
        resp = requests.get(update_url, timeout=timeout)
        resp.raise_for_status()
        log.info("FreeDNS-Update aufgerufen, Antwort: %s", resp.text.strip()[:200])
        return True
    except requests.RequestException as exc:
        log.error("FreeDNS-Update fehlgeschlagen: %s", exc)
        return False
