# Copyright (c) 2026 Stefan Koelle (https://stefankoelle.de)
# Licensed under the MIT License. See LICENSE file in project root for details.
import logging

import requests

log = logging.getLogger("healthcheck")


def ping(ping_url: str, status: str = "success", message: str = ""):
    if not ping_url:
        log.debug("Kein HEALTHCHECK_PING_URL konfiguriert - Ping wird ausgelassen.")
        return

    url = ping_url
    if status in ("fail", "partial-fail"):
        url = ping_url.rstrip("/") + "/fail"

    body = message or status
    try:
        requests.post(url, data=body.encode("utf-8"), timeout=5)
        log.debug("Healthcheck-Ping gesendet (%s): %s", status, message)
    except requests.RequestException as exc:
        log.warning("Healthcheck-Ping fehlgeschlagen: %s", exc)
