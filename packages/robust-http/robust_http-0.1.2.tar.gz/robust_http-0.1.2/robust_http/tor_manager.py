# ============ robust_http/tor_manager.py ============
"""
TorManager for applying SOCKS5 proxy and renewing circuits.
"""
import time
import socket
from typing import Optional
import requests
from stem import Signal
from stem.control import Controller

class TorManager:
    """Manage Tor proxy configuration and circuit renewal."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        socks_port: int = 9050,
        ctrl_port: int = 9051,
        password: Optional[str] = None,
    ):
        """Initialize TorManager.

        Args:
            host: Tor SOCKS host.
            socks_port: Tor SOCKS port.
            ctrl_port: Tor control port.
            password: Optional control port password.
        """
        self.host = host
        self.socks_proxy = f"socks5h://{host}:{socks_port}"
        self.ctrl_port = ctrl_port
        self.password = password
        self.can_renew = self._check_control_port()

    def _check_control_port(self) -> bool:
        """Check if Tor control port is reachable."""
        try:
            sock = socket.create_connection((self.host, self.ctrl_port), timeout=1)
            sock.close()
            return True
        except Exception:
            return False

    def apply_to_session(self, session: requests.Session) -> None:
        """Configure a requests.Session to route HTTP(S) over Tor."""
        session.proxies.update({
            "http":  self.socks_proxy,
            "https": self.socks_proxy,
        })

    def renew_circuit(self) -> None:
        """Signal Tor to build a new circuit (NEWNYM)."""
        if not self.can_renew:
            return
        try:
            with Controller.from_port(port=self.ctrl_port) as ctl:
                if self.password:
                    ctl.authenticate(password=self.password)
                else:
                    ctl.authenticate()
                ctl.set_conf("MaxCircuitDirtiness", "0")
                ctl.signal(Signal.NEWNYM)
            time.sleep(1.5)
        except Exception as e:
            print(f"⚠️ Tor renewal failed: {e}")

    def get_exit_ip(self) -> str:
        """Fetch current Tor exit IP via icanhazip.com."""
        sess = requests.Session()
        sess.proxies.update({
            "http":  self.socks_proxy,
            "https": self.socks_proxy,
        })
        resp = sess.get(
            "https://icanhazip.com",
            timeout=10,
            headers={"Cache-Control": "no-cache"},
        )
        return resp.text.strip()