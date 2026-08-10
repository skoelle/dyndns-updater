# Copyright (c) 2026 Stefan Koelle (https://stefankoelle.de)
# Licensed under the MIT License. See LICENSE file in project root for details.
import logging
import smtplib
from email.message import EmailMessage

from app.config import config

log = logging.getLogger("notify")


def send_ip_changed_email(old_ip: str | None, new_ip: str) -> bool:
    if not config.email_notification_enabled:
        log.debug("E-Mail-Notification nicht konfiguriert, überspringe.")
        return False

    if old_ip is None:
        old_ip = "unbekannt"

    subject = f"🌐 IP-Update: {old_ip} → {new_ip}"

    html = f"""\
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
             background: #0f172a; color: #e2e8f0; padding: 32px; margin: 0;">
  <div style="max-width: 480px; margin: 0 auto;">
    <div style="text-align: center; font-size: 48px; margin-bottom: 16px;">🔄</div>
    <h1 style="font-size: 20px; color: #38bdf8; text-align: center; margin-bottom: 24px;">
      IP-Adresse geändert
    </h1>
    <div style="background: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px;">
      <table style="width: 100%; border-collapse: collapse;">
        <tr>
          <td style="padding: 8px 0; color: #94a3b8; font-size: 14px;">📍 Alte IP</td>
          <td style="padding: 8px 0; text-align: right; font-family: monospace; font-size: 16px; color: #f87171;">
            {old_ip}
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding: 4px 0; text-align: center; font-size: 20px;">⬇️</td>
        </tr>
        <tr>
          <td style="padding: 8px 0; color: #94a3b8; font-size: 14px;">🆕 Neue IP</td>
          <td style="padding: 8px 0; text-align: right; font-family: monospace; font-size: 16px; color: #4ade80;">
            {new_ip}
          </td>
        </tr>
      </table>
    </div>
    <p style="font-size: 13px; color: #64748b; text-align: center; margin: 0;">
      📡 DynDNS-Updater · Cloudflare + FreeDNS aktualisiert
    </p>
  </div>
</body>
</html>"""

    text = f"IP-Adresse geändert: {old_ip} → {new_ip}"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config.notify_email_from
    msg["To"] = config.notify_email_to
    msg.set_content(text)
    msg.add_alternative(html, subtype="html")

    try:
        with smtplib.SMTP(config.smtp_host, config.smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(config.smtp_user, config.smtp_password)
            server.send_message(msg)
        log.info("E-Mail gesendet: %s -> %s", subject, config.notify_email_to)
        return True
    except Exception as exc:
        log.error("E-Mail-Versand fehlgeschlagen: %s", exc)
        return False
