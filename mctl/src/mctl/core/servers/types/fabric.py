import subprocess
from pathlib import Path

import typer
import requests

from .base import BaseInstaller

class FabricInstaller(BaseInstaller):
    name = "fabric"

    def get_download_url(self, version: str) -> str:
        url = "https://meta.fabricmc.net/v2/versions/installer"
        data = requests.get(url, timeout=10).json()
        latest_installer = data[0]["version"]
        return f"https://meta.fabricmc.net/v2/versions/installer/{latest_installer}"

    def install_fabric_server(self, java_path: str, dest_dir: Path, mc_version: str) -> None:
        """
        Runs the Fabric installer CLI to generate the fabric server files.
        """
        installer_jar = dest_dir / "fabric-installer.jar"
        typer.echo(f"☕ Running Fabric installer for Minecraft {mc_version}...")
        cmd = [
            java_path,
            "-jar",
            str(installer_jar),
            "server",
            "-mcversion",
            mc_version,
            "-downloadMinecraft"
        ]
        subprocess.run(cmd, cwd=dest_dir, check=True)
        typer.echo("Fabric server generated successfully.")

    def setup(self, base_downloads: Path, version: str, java_path: str, dest_dir: Path) -> None:
        """
        Handles downloading the installer, caching it, and running it.
        """
        dest_dir.mkdir(parents=True, exist_ok=True)
        installer_file = base_downloads / "fabric-installer.jar"

        # Download and cache the installer if not already
        if not installer_file.exists():
            typer.echo("Downloading Fabric installer...")
            url = self.get_download_url(version)
            r = requests.get(url, stream=True, timeout=120)
            r.raise_for_status()
            with open(installer_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            typer.echo(f"Saved Fabric installer to {installer_file}")
        else:
            typer.echo("Using cached Fabric installer.")

        # Copy installer into destination
        dest_copy = dest_dir / "fabric-installer.jar"
        if not dest_copy.exists():
            typer.echo("Copying installer to server directory.")
            dest_copy.write_bytes(installer_file.read_bytes())

        # Run the installer
        self.install_fabric_server(java_path, dest_dir, version)
        typer.echo("Fabric server setup complete.")
