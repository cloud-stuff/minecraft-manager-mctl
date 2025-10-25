import requests
from .base import BaseInstaller

class VanillaInstaller(BaseInstaller):
    name = "vanilla"

    def get_download_url(self, version: str) -> str:
        manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        manifest = requests.get(manifest_url, timeout=10).json()

        try:
            version_info = next(v for v in manifest["versions"] if v["id"] == version)
        except StopIteration as e:
            raise FileNotFoundError(f"Version {version} does not exist") from e

        version_json = requests.get(version_info["url"], timeout=10).json()
        return str(version_json["downloads"]["server"]["url"])
