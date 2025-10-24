import requests
from .base import BaseInstaller


class PaperInstaller(BaseInstaller):
    name = "paper"

    def get_download_url(self, version: str) -> str:
        api = f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds"
        builds = requests.get(api, timeout=10).json()["builds"]
        latest = builds[-1]
        build = latest["build"]
        file_name = latest["downloads"]["application"]["name"]
        return f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/{build}/downloads/{file_name}"
