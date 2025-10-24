from pathlib import Path
import shutil

import yaml

from mctl.core.constants import DEFAULT_HOME_PATH
from mctl.core.interfaces import ServerInfoResponse


class ServerRegistry:

    def __init__(self, base_path: Path = None):
        self.base = (base_path or DEFAULT_HOME_PATH).expanduser().resolve()

    def get_info(self, name: str) -> ServerInfoResponse:
        """
        Return metadata for a given server.
        Raises ServerNotFoundError if not found.
        """
        server_dir = self.base / "servers" / name
        meta_path = server_dir / "mcman.yaml"

        if not meta_path.exists():
            raise FileNotFoundError(f"Server '{name}' not found in {server_dir}")

        with open(meta_path) as f:
            meta = yaml.safe_load(f) or {}

        return ServerInfoResponse(**{
            "name": name,
            "path": str(server_dir),
            "type": meta.get("type"),
            "version": meta.get("version"),
            "memory": meta.get("memory"),
            "jar": meta.get("jar"),
            "java": meta.get("java", "java"),
        })

    def remove(self, name: str) -> None:
        server_dir = self.base / "servers" / name

        if not server_dir.exists():
            raise FileNotFoundError(f"Server '{name}' not found in {self.base}/servers/ directory")

        shutil.rmtree(server_dir)
