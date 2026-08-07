# Copyright (c) 2026 Stefan Koelle (https://stefankoelle.de)
# Licensed under the MIT License. See LICENSE file in project root for details.
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
        answer = resp.text.strip()[:200]
        if "has not changed" in answer:
            log.info("FreeDNS Webhook Response: IP unveraendert, nichts zu updaten.")
        else:
            log.info("FreeDNS-Update aufgerufen, Antwort: %s", answer)
        return True
    except requests.RequestException as exc:
        log.error("FreeDNS-Update fehlgeschlagen: %s", exc)
        return False
