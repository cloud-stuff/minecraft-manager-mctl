from typing import Optional

from mctl.core.constants import DEFAULT_HOME_PATH


class ServerConfigManager:
    """
    Handles reading and updating Minecraft server.properties files.
    """

    def __init__(self, server_name: str):
        self.server_dir = DEFAULT_HOME_PATH / "servers" / server_name
        self.config_path = self.server_dir / "server.properties"

        if not self.config_path.exists():
            raise FileNotFoundError(f"server.properties not found for '{server_name}'")

    def get(self, key: str) -> Optional[str]:
        """Return the value for a given key, or None if not found."""
        with open(self.config_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, v = line.split("=", 1)
                    if k.strip() == key:
                        return v.strip()
        return None

    def set(self, key: str, value: str) -> None:
        """Set or update a key=value pair in server.properties."""
        lines = []
        found = False

        if self.config_path.exists():
            with open(self.config_path) as f:
                for line in f:
                    if line.strip().startswith(f"{key}="):
                        lines.append(f"{key}={value}\n")
                        found = True
                    else:
                        lines.append(line)

        if not found:
            lines.append(f"{key}={value}\n")

        with open(self.config_path, "w") as f:
            f.writelines(lines)
