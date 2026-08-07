# Copyright (c) 2026 Stefan Koelle (https://stefankoelle.de)
# Licensed under the MIT License. See LICENSE file in project root for details.
import logging

import requests

log = logging.getLogger("cloudflare")

API_BASE = "https://api.cloudflare.com/client/v4"


class CloudflareError(Exception):
    pass


def _headers(api_token: str):
    return {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }


def _find_record_id(zone_id: str, api_token: str, name: str):
    url = f"{API_BASE}/zones/{zone_id}/dns_records"
    resp = requests.get(
        url, headers=_headers(api_token), params={"type": "A", "name": name}, timeout=15
    )
    resp.raise_for_status()
    data = resp.json()
    results = data.get("result", [])
    if not results:
        return None
    if len(results) > 1:
        log.warning(
            "Mehrere A-Records fuer '%s' gefunden (%d), nur erster wird aktualisiert.",
            name,
            len(results),
        )
    return results[0]["id"]


def update_records(zone_id: str, api_token: str, record_names, ip: str) -> dict:
    results = {}
    for name in record_names:
        try:
            record_id = _find_record_id(zone_id, api_token, name)
            if record_id is None:
                results[name] = "error: Record nicht gefunden (existiert der A-Record bereits?)"
                log.error("Cloudflare-Record nicht gefunden: %s", name)
                continue

            url = f"{API_BASE}/zones/{zone_id}/dns_records/{record_id}"
            payload = {
                "type": "A",
                "name": name,
                "content": ip,
                "proxied": False,
                "ttl": 60,
            }
            resp = requests.put(url, headers=_headers(api_token), json=payload, timeout=15)
            resp.raise_for_status()
            body = resp.json()
            if not body.get("success"):
                results[name] = f"error: {body.get('errors')}"
                log.error("Cloudflare-Update fehlgeschlagen fuer %s: %s", name, body.get("errors"))
                continue

            results[name] = "ok"
            log.info("Cloudflare-Record aktualisiert: %s -> %s", name, ip)
        except requests.RequestException as exc:
            results[name] = f"error: {exc}"
            log.error("Cloudflare-API-Fehler fuer %s: %s", name, exc)

    return results
