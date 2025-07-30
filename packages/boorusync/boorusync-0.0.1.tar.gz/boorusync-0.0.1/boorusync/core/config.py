import os
import configparser
import platform
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from dotenv import load_dotenv
import re
import subprocess
from urllib.parse import urlparse


class Config:
    """
    Configuration handler for booru-sync.
    Manages settings in ~/.config/booru-sync/settings.ini.
    """

    # Placeholder configuration values organized by section
    VALUES = {
        "general": {
            "debug": "False",
            "user_agent": "booru-sync/1.0",
        },
        "network": {
            "timeout": "30",
            "proxy": "",
            "retry_count": "3",
            "enable_proxy_detection": "True",
            "max_concurrent_requests": "5",
            "default_timeout": "30",
        },
        "paths": {
            "default_download_dir": str(Path.home() / "Downloads"),
        },
        "sync": {
            "sync_interval": "3600",
        },
    }

    NUMBER_SETTINGS = {"timeout", "retry_count", "sync_interval", "max_items_per_sync"}

    def __init__(self):
        load_dotenv()
        self.config = configparser.ConfigParser()
        self.config_path = self._get_config_path()
        self._config_accessible = True
        self.ensure_config_exists()
        self.load_config()

    def _get_config_dir(self) -> Path:
        """
        Determine the configuration directory based on the environment and platform.
        Returns:
            Path: The path to the configuration directory.
        """
        if os.getenv("BOORU_SYNC_CONFIG_DIR"):
            return Path(os.getenv("BOORU_SYNC_CONFIG_DIR"))
        system = platform.system()
        if system == "Windows":
            return Path(os.getenv("APPDATA", Path.home())) / "booru-sync"
        elif system == "Darwin":
            return Path.home() / "Library" / "Application Support" / "booru-sync"
        return Path.home() / ".config" / "booru-sync"

    def _get_config_path(self) -> Path:
        if os.getenv("BOORU_SYNC_CONFIG_PATH"):
            return Path(os.getenv("BOORU_SYNC_CONFIG_PATH"))
        return self._get_config_dir() / "settings.ini"

    def ensure_config_exists(self) -> None:
        config_dir = self.config_path.parent
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            for section, options in self.VALUES.items():
                self.config[section] = options
            self.save_config()

    def load_config(self) -> None:
        if self.config_path.exists():
            self.config.read(self.config_path)

    def save_config(self) -> None:
        if not self._config_accessible:
            return
        with open(self.config_path, "w") as config_file:
            self.config.write(config_file)

    def get(self, option: str, fallback: Any = None, section: Optional[str] = None) -> Union[str, int, float, bool]:
        load_dotenv()
        section = section or next((s for s in self.VALUES if option in self.VALUES[s]), "general")
        env_var = f"BOORU_SYNC_{section.upper()}_{option.upper()}"
        if env_var in os.environ:
            return os.getenv(env_var)
        if self.config.has_option(section, option):
            value = self.config.get(section, option)
            if option in self.NUMBER_SETTINGS:
                try:
                    return int(value) if value.isdigit() else float(value)
                except ValueError:
                    pass
            if value.lower() in ("true", "false"):
                return value.lower() == "true"
            return value
        return fallback or self.VALUES.get(section, {}).get(option)

    def get_as_number(self, option: str, section: Optional[str] = None) -> Optional[Union[int, float]]:
        section = section or next((s for s in self.VALUES if option in self.VALUES[s]), "general")
        value = self.get(option, section=section)
        if value is None:
            return None
        try:
            return int(value) if value.isdigit() else float(value)
        except ValueError:
            return None

    def set(self, option: str, value: str, section: Optional[str] = None) -> None:
        section = section or next((s for s in self.VALUES if option in self.VALUES[s]), "general")
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, option, value)
        self.save_config()

    def reset_to_default(self, option: str, section: Optional[str] = None) -> bool:
        section = section or next((s for s in self.VALUES if option in self.VALUES[s]), "general")
        if section in self.VALUES and option in self.VALUES[section]:
            self.set(option, self.VALUES[section][option], section)
            return True
        return False

    def reset_all_to_defaults(self) -> None:
        for section, options in self.VALUES.items():
            self.config[section] = options
        self.save_config()

    def get_all_settings(self) -> Dict[str, Dict[str, str]]:
        return {section: dict(self.config[section]) for section in self.config.sections()}

    def _detect_system_proxy(self) -> Optional[str]:
        """
        Detect system proxy settings from environment variables or OS settings.
        Returns:
            Optional[str]: A proxy URL string or None if no proxy is detected.
        """
        # 1. Check environment variables
        for env_var in [
            "https_proxy",
            "HTTPS_PROXY",
            "http_proxy",
            "HTTP_PROXY",
            "all_proxy",
            "ALL_PROXY",
        ]:
            if env_var in os.environ and os.environ[env_var]:
                return self._normalize_proxy_url(os.environ[env_var])

        # 2. Platform-specific detection
        system = platform.system()
        if system == "Windows":
            try:
                import winreg

                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(
                    registry,
                    r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                )
                proxy_enabled = winreg.QueryValueEx(key, "ProxyEnable")[0]
                if proxy_enabled:
                    proxy_server = winreg.QueryValueEx(key, "ProxyServer")[0]
                    return self._normalize_proxy_url(proxy_server)
            except Exception as e:
                print(f"Error detecting Windows proxy: {e}")
        elif system == "Darwin":
            try:
                result = subprocess.run(
                    ["networksetup", "-getwebproxy", "Wi-Fi"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    output = result.stdout
                    enabled_match = re.search(r"Enabled:\s*(Yes|No)", output)
                    server_match = re.search(r"Server:\s*([^\n]+)", output)
                    port_match = re.search(r"Port:\s*(\d+)", output)
                    if enabled_match and enabled_match.group(1) == "Yes" and server_match and port_match:
                        server = server_match.group(1).strip()
                        port = port_match.group(1).strip()
                        return f"http://{server}:{port}"
            except Exception as e:
                print(f"Error detecting macOS proxy: {e}")
        elif system == "Linux":
            try:
                result = subprocess.run(
                    ["gsettings", "get", "org.gnome.system.proxy", "mode"],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0 and "manual" in result.stdout:
                    http_host = (
                        subprocess.run(
                            ["gsettings", "get", "org.gnome.system.proxy.http", "host"],
                            capture_output=True,
                            text=True,
                        )
                        .stdout.strip()
                        .strip("'")
                    )
                    http_port = subprocess.run(
                        ["gsettings", "get", "org.gnome.system.proxy.http", "port"],
                        capture_output=True,
                        text=True,
                    ).stdout.strip()
                    if http_host and http_port:
                        return f"http://{http_host}:{http_port}"
            except Exception as e:
                print(f"Error detecting Linux proxy: {e}")
        return None

    def _normalize_proxy_url(self, proxy_url: str) -> Optional[str]:
        """
        Normalize proxy URL to a standard format.
        Args:
            proxy_url (str): The proxy URL to normalize.
        Returns:
            Optional[str]: The normalized proxy URL or None if invalid.
        """
        if not re.match(r"^[a-zA-Z]+://", proxy_url):
            proxy_url = f"http://{proxy_url}"
        parsed = urlparse(proxy_url)
        if not parsed.hostname:
            return None
        if not parsed.port:
            port = 80 if parsed.scheme == "http" else 443
            proxy_url = f"{parsed.scheme}://{parsed.hostname}:{port}"
        return proxy_url

    def _is_localhost_url(self, url: str) -> bool:
        """
        Check if a URL points to a localhost address.
        Args:
            url (str): The URL to check.
        Returns:
            bool: True if the URL points to localhost, False otherwise.
        """
        if not url:
            return False
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if not hostname:
            return False
        if hostname in ("localhost", "host.docker.internal", "::1", "[::1]", "0.0.0.0"):
            return True
        if hostname.startswith("127."):
            return True
        return False

    def get_effective_proxy(self, url: str, explicit_proxy: Optional[str] = None) -> Optional[str]:
        """
        Determine the effective proxy to use for a given URL, considering bypass for localhost.
        """
        bypass = self.get("bypass_proxy_for_localhost", True, section="network")
        proxy_detection_enabled = self.get("enable_proxy_detection", True, section="network")
        proxy = explicit_proxy if explicit_proxy is not None else self.get("proxy", section="network")
        if not proxy and proxy_detection_enabled:
            proxy = self._detect_system_proxy()
        if bypass and self._is_localhost_url(url):
            return None
        return proxy
