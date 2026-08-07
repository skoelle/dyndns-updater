import logging
import time

from fritzconnection import FritzConnection
from fritzconnection.core.exceptions import FritzConnectionException

log = logging.getLogger("fritzbox")


class FritzBoxError(Exception):
    pass


def get_external_ip(
    host: str, port: int, user: str, password: str, retries: int = 3, backoff_seconds=(2, 5, 10)
) -> str:
    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            fc = FritzConnection(address=host, port=port, user=user, password=password)
            result = fc.call_action("WANIPConn1", "GetExternalIPAddress")
            ip = result.get("NewExternalIPAddress")
            if not ip:
                raise FritzBoxError("Leere Antwort von der FritzBox (kein NewExternalIPAddress)")
            log.info("Externe IP von FritzBox erhalten: %s (Versuch %d/%d)", ip, attempt, retries)
            return ip
        except (FritzConnectionException, FritzBoxError, OSError) as exc:
            last_exc = exc
            log.warning("TR-064-Abfrage fehlgeschlagen (Versuch %d/%d): %s", attempt, retries, exc)
            if attempt < retries:
                sleep_time = backoff_seconds[min(attempt - 1, len(backoff_seconds) - 1)]
                time.sleep(sleep_time)

    raise FritzBoxError(f"Konnte externe IP nach {retries} Versuchen nicht ermitteln: {last_exc}")
