from .base import BaseInstaller

class PurpurInstaller(BaseInstaller):
    name = "purpur"

    def get_download_url(self, version: str) -> str:
        url = f"https://api.purpurmc.org/v2/purpur/{version}/latest/download"
        # The Purpur API redirects to a binary, so we can return it directly
        return url
