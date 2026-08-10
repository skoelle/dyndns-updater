# Copyright (c) 2026 Stefan Koelle (https://stefankoelle.de)
# Licensed under the MIT License. See LICENSE file in project root for details.
import logging
import os
import sys

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

log = logging.getLogger("config")

REQUIRED_VARS = [
    "FRITZBOX_HOST",
    "FRITZBOX_USER",
    "FRITZBOX_PASSWORD",
    "CLOUDFLARE_API_TOKEN",
    "CLOUDFLARE_ZONE_ID",
    "CLOUDFLARE_RECORDS",
]


class Config:
    def __init__(self):
        self.fritzbox_host = os.environ.get("FRITZBOX_HOST", "192.168.178.1")
        self.fritzbox_port = int(os.environ.get("FRITZBOX_PORT", "49000"))
        self.fritzbox_user = os.environ.get("FRITZBOX_USER")
        self.fritzbox_password = os.environ.get("FRITZBOX_PASSWORD")

        self.cloudflare_api_token = os.environ.get("CLOUDFLARE_API_TOKEN")
        self.cloudflare_zone_id = os.environ.get("CLOUDFLARE_ZONE_ID")
        records_raw = os.environ.get("CLOUDFLARE_RECORDS", "")
        self.cloudflare_records = [r.strip() for r in records_raw.split(",") if r.strip()]

        self.freedns_update_url = os.environ.get("FREEDNS_UPDATE_URL", "")

        self.poll_interval_minutes = int(os.environ.get("POLL_INTERVAL_MINUTES", "15"))

        self.healthcheck_ping_url = os.environ.get("HEALTHCHECK_PING_URL", "")

        self.smtp_host = os.environ.get("SMTP_HOST", "")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.smtp_user = os.environ.get("SMTP_USER", "")
        self.smtp_password = os.environ.get("SMTP_PASSWORD", "")
        self.notify_email_to = os.environ.get("NOTIFY_EMAIL_TO", "")
        self.notify_email_from = os.environ.get("NOTIFY_EMAIL_FROM", "")

        self.state_path = os.environ.get("STATE_PATH", "/app/data/last-known-ip.json")

    @property
    def email_notification_enabled(self) -> bool:
        return bool(self.smtp_host and self.notify_email_to and self.notify_email_from)

    def validate(self):
        missing = [v for v in REQUIRED_VARS if not os.environ.get(v)]
        if missing:
            log.error("Fehlende Pflicht-ENV-Variablen: %s", ", ".join(missing))
            sys.exit(1)
        if not self.cloudflare_records:
            log.error("CLOUDFLARE_RECORDS ist leer - mindestens eine Subdomain angeben.")
            sys.exit(1)
        log.info(
            "Konfiguration geladen: %d Cloudflare-Record(s), Poll-Intervall=%d Min",
            len(self.cloudflare_records),
            self.poll_interval_minutes,
        )


config = Config()
