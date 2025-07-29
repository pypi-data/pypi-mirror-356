import json
from pathlib import Path
from dataclasses import dataclass

from aiomexc import Credentials


CONFIG_DIR = Path.home() / ".config" / "aiomexc"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
ACTIVE_CREDENTIALS_FILE = CONFIG_DIR / "active_credentials.json"


@dataclass
class CliCredentials(Credentials):
    name: str
    socks5_proxy: str | None = None

    def __post_init__(self):
        self.name = self.name.lower()


class CredentialsManager:
    def __init__(self):
        self._credentials = self._load_credentials()
        self._active_credentials = self._get_active_credentials()

    def _load_credentials(self) -> dict[str, CliCredentials]:
        if not CREDENTIALS_FILE.exists():
            return {}

        with Path(CREDENTIALS_FILE).open() as f:
            data = json.load(f)
            return {
                name: CliCredentials(
                    name=name,
                    access_key=credentials["access_key"],
                    secret_key=credentials["secret_key"],
                    socks5_proxy=credentials.get("socks5_proxy"),
                )
                for name, credentials in data.items()
            }

    def _get_active_credentials(self) -> CliCredentials | None:
        if not ACTIVE_CREDENTIALS_FILE.exists():
            return None

        with Path(ACTIVE_CREDENTIALS_FILE).open() as f:
            data = json.load(f)
            return self._credentials.get(data.get("name"))

    def _dump_credentials(self) -> dict[str, dict]:
        return {
            name: {
                "access_key": credentials.access_key,
                "secret_key": credentials.secret_key,
                "socks5_proxy": credentials.socks5_proxy,
            }
            for name, credentials in self._credentials.items()
        }

    def _save_credentials(self) -> None:
        with Path(CREDENTIALS_FILE).open("w") as f:
            json.dump(self._dump_credentials(), f, indent=2)

    def get_active_credentials(self) -> CliCredentials | None:
        """
        Get the active credentials. If no active credentials are set, return the first
        credentials in the list.
        """
        if self._active_credentials is not None:
            return self._active_credentials

        if not self._credentials:
            return None

        return next(iter(self._credentials.values()))

    def list_credentials(self) -> list[CliCredentials]:
        return list(self._credentials.values())

    def save_credentials(self, credentials: CliCredentials) -> None:
        self._credentials[credentials.name] = credentials
        self._save_credentials()

    def delete_credentials(self, name: str) -> None:
        credentials = self._credentials.pop(name, None)
        if credentials is not None:
            self._save_credentials()

    def set_active_credentials(self, credentials: CliCredentials) -> None:
        self._active_credentials = credentials

        with Path(ACTIVE_CREDENTIALS_FILE).open("w") as f:
            json.dump({"name": credentials.name}, f, indent=2)
