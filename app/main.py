import concurrent.futures
import logging
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from app import cloudflare, freedns, healthcheck, state
from app.config import config
from app.fritzbox import FritzBoxError, get_external_ip

log = logging.getLogger("main")

app = Flask(__name__)

_lock = threading.Lock()
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)


def run_cycle(trigger: str = "unknown"):
    with _lock:
        log.info("Starte Update-Zyklus (Trigger=%s)", trigger)
        try:
            current_ip = get_external_ip(
                config.fritzbox_host,
                config.fritzbox_port,
                config.fritzbox_user,
                config.fritzbox_password,
            )
        except FritzBoxError as exc:
            log.error("IP-Ermittlung fehlgeschlagen: %s", exc)
            healthcheck.ping(config.healthcheck_ping_url, status="fail", message=str(exc))
            return

        last_ip = state.load(config.state_path)

        if last_ip is None:
            log.info("Erstlauf - IP wird gesetzt: %s", current_ip)
        elif current_ip == last_ip:
            log.info("IP unveraendert (%s) - kein DNS-Update noetig.", current_ip)
            if trigger == "poll":
                healthcheck.ping(
                    config.healthcheck_ping_url,
                    status="success",
                    message=f"alive, ip unchanged ({current_ip})",
                )
            return

        log.info("IP-Aenderung erkannt: %s -> %s", last_ip, current_ip)

        cf_results = cloudflare.update_records(
            config.cloudflare_zone_id,
            config.cloudflare_api_token,
            config.cloudflare_records,
            current_ip,
        )
        cf_ok = all(v == "ok" for v in cf_results.values())

        freedns_ok = freedns.update(config.freedns_update_url)

        if cf_ok and freedns_ok:
            state.save(config.state_path, current_ip)
            healthcheck.ping(
                config.healthcheck_ping_url,
                status="success",
                message=f"IP updated to {current_ip}",
            )
        else:
            failed = {k: v for k, v in cf_results.items() if v != "ok"}
            log.error(
                "Update unvollstaendig - state wird NICHT gespeichert. "
                "Cloudflare-Fehler: %s, FreeDNS ok=%s",
                failed,
                freedns_ok,
            )
            healthcheck.ping(
                config.healthcheck_ping_url,
                status="partial-fail",
                message=f"partial failure: cf_errors={failed} freedns_ok={freedns_ok}",
            )


@app.route("/webhook/update", methods=["GET"])
def webhook_update():
    _executor.submit(run_cycle, trigger="webhook")
    return {"status": "triggered"}, 202


@app.route("/healthz", methods=["GET"])
def healthz():
    return {"status": "ok"}, 200


def main():
    config.validate()

    log.info("Initial-Update-Zyklus beim Start...")
    run_cycle(trigger="startup")

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_cycle,
        "interval",
        minutes=config.poll_interval_minutes,
        kwargs={"trigger": "poll"},
        id="fallback-poll",
    )
    scheduler.start()
    log.info("Fallback-Polling gestartet (alle %d Minuten).", config.poll_interval_minutes)

    log.info(
        "Webhook-Server startet auf Port %d (GET /webhook/update, kein Auth).", config.webhook_port
    )
    app.run(host="0.0.0.0", port=config.webhook_port)


if __name__ == "__main__":
    main()
