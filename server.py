import json
import traceback
import datetime
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))

def log(msg):
    line = f"[{datetime.datetime.now()}] {msg}"
    print(line, flush=True)

class H(BaseHTTPRequestHandler):
    def _send_json(self, resp_str):
        data = resp_str.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        log(f"GET {self.path}")
        self._send_json(json.dumps({"status": "ok"}))

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length else b''
            body_str = body.decode('utf-8', errors='replace')
            log(f"POST {self.path} len={length} body={body_str}")
            path = self.path

            if '/login-access' in path:
                resp = json.dumps([{
                    "status": "enable",
                    "username": "xhfhcgh",
                    "remaining_time": "9999999999",
                    "user_id": "12345",
                    "token": "testtoken123",
                    "check-user": "ok",
                    "geo_restricted": False,
                    "icon_base": "",
                    "image_base": "",
                    "telegram_base": "https://t.me/",
                    "whatsapp_base": "https://wa.me/",
                    "telegram": "https://t.me/ninjasupport",
                    "technical_support": "https://t.me/ninjasupport",
                    "regions": [{
                        "name": "Global",
                        "icon": "",
                        "resellers": [{
                            "un": "Admin",
                            "telegram_id": "ninjasupport",
                            "whatsapp_id": "1234567890"
                        }]
                    }]
                }])

            elif '/check-version' in path:
                resp = json.dumps({
                    "check-user": "ok",
                    "app-1": {
                        "version-app": "2.1.0",
                        "URL Update": ""
                    }
                })

            elif '/social-info' in path:
                resp = json.dumps([{
                    "telegram": "https://t.me/ninjasupport",
                    "technical_support": "https://t.me/ninjasupport",
                    "whatsapp": "https://wa.me/1234567890",
                    "discord": "https://discord.gg/ninja"
                }])

            elif '/reseller-list' in path:
                resp = json.dumps([{
                    "result": 9,
                    "check-user": "ok",
                    "icon_base": "",
                    "image_base": "",
                    "telegram_base": "https://t.me/",
                    "whatsapp_base": "https://wa.me/",
                    "regions": [{
                        "name": "Global",
                        "icon": "",
                        "resellers": [{
                            "un": "Admin",
                            "telegram_id": "ninjasupport",
                            "whatsapp_id": "1234567890"
                        }]
                    }]
                }])

            elif '/alert-feed' in path:
                resp = json.dumps([{
                    "result": 9,
                    "check-user": "ok",
                    "messages": []
                }])

            elif '/logcat' in path:
                resp = json.dumps({"status": "ok"})

            else:
                resp = json.dumps({"status": "ok"})

            self._send_json(resp)
            log(f"  -> OK")
        except Exception as e:
            log(f"  -> ERROR: {e}")
            traceback.print_exc()
            try:
                self.send_response(500)
                self.end_headers()
            except:
                pass

    def log_message(self, *a):
        pass

log(f"NINJA SERVER STARTED ON PORT {PORT}")
HTTPServer(('0.0.0.0', PORT), H).serve_forever()
