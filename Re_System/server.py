#!/usr/bin/env python3
"""Lokaler Python-Server für Re_System 1.0."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from datetime import datetime, timezone
import json
import shutil

BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / "backups"

HOST = "127.0.0.1"
PORT = 8000

DEFAULT_RE1 = {
    "schemaVersion": 1,
    "datensatz": "Re1",
    "person": {
        "vorname": "",
        "nachname": ""
    }
}

DEFAULT_RE2 = {
    "schemaVersion": 1,
    "datensatz": "Re2",
    "kontakt": {
        "strasse": "",
        "hausnummer": "",
        "plz": "",
        "ort": "",
        "land": ""
    }
}


def read_json(filename, default):
    path = BASE_DIR / filename

    if not path.exists():
        return default

    content = path.read_text(encoding="utf-8").strip()

    if not content:
        return default

    return json.loads(content)


class Handler(BaseHTTPRequestHandler):

    def send_json(self, status, payload):
        body = json.dumps(
            payload,
            ensure_ascii=False,
            indent=2
        ).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):

        if self.path == "/api/data":
            try:
                self.send_json(200, {
                    "re1": read_json("Re1.json", DEFAULT_RE1),
                    "re2": read_json("Re2.json", DEFAULT_RE2)
                })

            except (json.JSONDecodeError, OSError) as exc:
                self.send_json(500, {
                    "error": f"JSON-Datei kann nicht gelesen werden: {exc}"
                })

            return

        if self.path in ("/", "/Re3.html"):
            page = (BASE_DIR / "Re3.html").read_bytes()

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
            return

        self.send_error(404, "Nicht gefunden")

    def do_POST(self):

        if self.path != "/api/save":
            self.send_error(404, "Nicht gefunden")
            return

        try:
            length = int(
                self.headers.get("Content-Length", "0")
            )

            if length <= 0 or length > 100_000:
                self.send_json(400, {
                    "error": "Ungültige Datenmenge."
                })
                return

            payload = json.loads(
                self.rfile.read(length).decode("utf-8")
            )

            re1 = payload["re1"]
            re2 = payload["re2"]

            # Nur die vorgesehenen Felder übernehmen.
            clean_re1 = {
                "schemaVersion": 1,
                "datensatz": "Re1",
                "person": {
                    "vorname": str(
                        re1["person"].get("vorname", "")
                    ),
                    "nachname": str(
                        re1["person"].get("nachname", "")
                    )
                }
            }

            clean_re2 = {
                "schemaVersion": 1,
                "datensatz": "Re2",
                "kontakt": {
                    key: str(re2["kontakt"].get(key, ""))
                    for key in (
                        "strasse",
                        "hausnummer",
                        "plz",
                        "ort",
                        "land"
                    )
                }
            }

            # Sicherungskopien anlegen.
            BACKUP_DIR.mkdir(exist_ok=True)

            stamp = datetime.now(
                timezone.utc
            ).strftime("%Y%m%dT%H%M%S_%fZ")

            backups = []

            for filename in ("Re1.json", "Re2.json"):
                source = BASE_DIR / filename

                if (
                    source.exists()
                    and source.read_text(
                        encoding="utf-8"
                    ).strip()
                ):
                    backup = (
                        BACKUP_DIR /
                        f"{filename}.{stamp}.bak"
                    )

                    shutil.copy2(source, backup)
                    backups.append(
                        str(backup.relative_to(BASE_DIR))
                    )

            # Temporär schreiben und atomar ersetzen.
            for filename, data in (
                ("Re1.json", clean_re1),
                ("Re2.json", clean_re2)
            ):
                target = BASE_DIR / filename

                temporary = target.with_suffix(
                    target.suffix + ".tmp"
                )

                temporary.write_text(
                    json.dumps(
                        data,
                        ensure_ascii=False,
                        indent=2
                    ) + "\n",
                    encoding="utf-8"
                )

                temporary.replace(target)

            self.send_json(200, {
                "ok": True,
                "backups": backups
            })

        except (
            KeyError,
            TypeError,
            ValueError,
            json.JSONDecodeError,
            OSError
        ) as exc:
            self.send_json(400, {
                "error": f"Speichern fehlgeschlagen: {exc}"
            })


if __name__ == "__main__":
    print(
        f"Re_System läuft lokal auf http://{HOST}:{PORT}"
    )
    print("Beenden mit Strg+C")

    ThreadingHTTPServer(
        (HOST, PORT),
        Handler
    ).serve_forever()
