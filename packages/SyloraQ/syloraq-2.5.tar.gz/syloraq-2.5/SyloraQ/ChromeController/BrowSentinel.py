import os
import sys
import time
import json
import socket
import struct
import base64
import threading
import subprocess
import http.client
import shutil
import hashlib

class SimpleWebSocketClient:
    def __init__(self, ws_url):
        _, rest = ws_url.split('://', 1)
        hostport, path = rest.split('/', 1)
        if ':' in hostport:
            self.host, port = hostport.split(':')
            self.port = int(port)
        else:
            self.host = hostport
            self.port = 80
        self.path = '/' + path
        self.sock = None
        self.connected = False
        self.running = False
        self.pending = {}
        self.next_id = 1
        self.lock = threading.Lock()
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            f"GET {self.path} HTTP/1.1\r\n"
            f"Host: {self.host}:{self.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n"
            "\r\n"
        )
        sock.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            chunk = sock.recv(4096)
            if not chunk:raise RuntimeError("Handshake failed: socket closed")
            buf += chunk
        self.sock = sock
        self.connected = True
        self.running = True
        threading.Thread(target=self._recv_loop, daemon=True).start()
    def _recv_exact(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:raise RuntimeError("Socket closed during recv")
            buf += chunk
        return buf
    def _recv_frame(self):
        hdr = self._recv_exact(2)
        b1, b2 = hdr
        masked = b2 & 0x80
        length = b2 & 0x7F
        if length == 126:length = struct.unpack(">H", self._recv_exact(2))[0]
        elif length == 127:length = struct.unpack(">Q", self._recv_exact(8))[0]
        mask = self._recv_exact(4) if masked else None
        payload = self._recv_exact(length)
        if mask:payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        opcode = b1 & 0x0F
        if opcode == 0x8:
            self.close()
            return None
        if opcode == 0x9:
            self._send_frame(0x8A, payload)
            return None
        if opcode != 0x1:return None
        return payload.decode('utf-8', errors='ignore')
    def _recv_loop(self):
        while self.running:
            try:
                msg = self._recv_frame()
                if msg is None:break
                data = json.loads(msg)
                if 'id' in data and data['id'] in self.pending:
                    slot = self.pending[data['id']]
                    slot['resp'] = data
                    slot['event'].set()
            except Exception as e:break
        self.running = False
        self.connected = False
    def _send_frame(self, first_byte, payload: bytes):
        header = bytes([first_byte])
        length = len(payload)
        if length < 126:header += bytes([0x80 | length])
        elif length < (1 << 16):header += bytes([0x80 | 126]) + struct.pack(">H", length)
        else:header += bytes([0x80 | 127]) + struct.pack(">Q", length)
        mask = os.urandom(4)
        header += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(header + masked)
    def send(self, method, params=None, timeout=5):
        if not self.connected:raise RuntimeError("WebSocket not connected")
        with self.lock:
            msg_id = self.next_id
            self.next_id += 1
        msg = {"id": msg_id, "method": method}
        if params is not None:msg["params"] = params
        text = json.dumps(msg).encode('utf-8')
        frame = bytearray([0x81])
        L = len(text)
        if L < 126:frame.append(0x80 | L)
        elif L < (1 << 16):
            frame.append(0x80 | 126)
            frame.extend(struct.pack(">H", L))
        else:
            frame.append(0x80 | 127)
            frame.extend(struct.pack(">Q", L))
        mask = os.urandom(4)
        frame.extend(mask)
        frame.extend(b ^ mask[i % 4] for i, b in enumerate(text))
        ev = threading.Event()
        self.pending[msg_id] = {"event": ev, "resp": None}
        self.sock.sendall(frame)
        if not ev.wait(timeout):
            self.pending.pop(msg_id, None)
            raise TimeoutError(f"{method} timed out")
        resp = self.pending[msg_id]["resp"]
        del self.pending[msg_id]
        if "error" in resp:raise RuntimeError(f"{method} error: {resp['error']}")
        return resp
    def close(self):
        self.running = False
        try:self.sock.close()
        except:pass
class BrowSentinel:
    def __init__(self, headless=True, port=8381):
        self.headless = headless
        self.port = port
        self.proc = None
        self.ws = None
    def _find_chrome(self):
        if sys.platform.startswith("win"):
            p = os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe")
            return p if os.path.exists(p) else None
        elif sys.platform == "darwin":
            p = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            return p if os.path.exists(p) else None
        else:return shutil.which("google-chrome")
    def start(self):
        chrome = self._find_chrome()
        if not chrome:raise RuntimeError("Chrome not found")
        args = [chrome, f"--remote-debugging-port={self.port}", "--disable-gpu"]
        if self.headless:args.append("--headless=new")
        args.append("about:blank")
        self.proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        conn = http.client.HTTPConnection("localhost", self.port)
        conn.request("GET", "/json")
        targets = json.loads(conn.getresponse().read())
        page = next(t for t in targets if t.get("type") == "page")
        ws_url = page["webSocketDebuggerUrl"]
        self.ws = SimpleWebSocketClient(ws_url)
        self.ws.connect()
        self.ws.send("Page.enable")
        self.ws.send("DOM.enable")
        self.ws.send("Network.enable")
    def navigate(self, url):return self.ws.send("Page.navigate", {"url": url})
    def reload(self):return self.ws.send("Page.reload")
    def back(self):
        history = self.ws.send("Page.getNavigationHistory")
        entries = history["result"]["entries"]
        idx = history["result"]["currentIndex"]
        if idx <= 0:raise RuntimeError("No back history entry")
        entry_id = entries[idx-1]["id"]
        return self.ws.send("Page.navigateToHistoryEntry", {"entryId": entry_id})
    def forward(self):
        history = self.ws.send("Page.getNavigationHistory")
        entries = history["result"]["entries"]
        idx = history["result"]["currentIndex"]
        if idx >= len(entries) - 1: raise RuntimeError("No forward history entry")
        entry_id = entries[idx+1]["id"]
        return self.ws.send("Page.navigateToHistoryEntry", {"entryId": entry_id})
    def set_viewport(self, width, height, deviceScaleFactor=1):return self.ws.send("Emulation.setDeviceMetricsOverride", {"width": width, "height": height,"deviceScaleFactor": deviceScaleFactor,"mobile": False})
    def evaluate(self, script):
        resp = self.ws.send("Runtime.evaluate", {"expression": script, "returnByValue": True})
        return resp.get("result", {}).get("result", {}).get("value")
    def get_html(self):
        resp = self.ws.send("DOM.getDocument")
        node_id = resp["result"]["root"]["nodeId"]
        outer = self.ws.send("DOM.getOuterHTML", {"nodeId": node_id})
        return outer["result"]["outerHTML"]
    def get_text(self):
        return self.evaluate("document.body.innerText")
    def click(self, selector):
        return self.evaluate(f"document.querySelector('{selector}').click()")
    def type(self, selector, text):
        js = (f"(el=document.querySelector('{selector}')).value='{text}';""el.dispatchEvent(new Event('input'));")
        return self.evaluate(js)
    def wait_for(self, selector, timeout=5):
        js = (
            "(sel,to)=>new Promise((res, rej)=>{"
            "let t=0; function check(){"
            "if(document.querySelector(sel)) return res(true);"
            "if(t>to*1000) return rej('timeout');""t+=100; setTimeout(check,100);} check();})")
        return self.evaluate(f"({js})('{selector}',{timeout})")
    def screenshot(self, path="page.png"):
        self.ws.send("Page.captureScreenshot")
        resp = self.ws.send("Page.captureScreenshot")
        data = resp["result"]["data"]
        with open(path, "wb") as f:f.write(base64.b64decode(data))
        return path
    def close(self):
        if self.ws:self.ws.close()
        if self.proc:
            self.proc.terminate()
            self.proc.wait()