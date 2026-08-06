import json
import logging
import os

log = logging.getLogger("state")


def load(state_path: str):
    if not os.path.exists(state_path):
        log.info("Keine vorherige State-Datei gefunden (%s) - Erstlauf.", state_path)
        return None
    try:
        with open(state_path, "r") as f:
            data = json.load(f)
        return data.get("last_ip")
    except (json.JSONDecodeError, OSError) as exc:
        log.warning("State-Datei konnte nicht gelesen werden (%s): %s", state_path, exc)
        return None


def save(state_path: str, ip: str):
    os.makedirs(os.path.dirname(state_path), exist_ok=True)
    with open(state_path, "w") as f:
        json.dump({"last_ip": ip}, f)
    log.info("State gespeichert: last_ip=%s", ip)
