import pkgutil
import importlib
import shutil
import subprocess
import time
from pathlib import Path
import requests
import yaml

from mctl.core.exceptions import InvalidCliArgument


class ServerInstaller:

    SERVER_TYPES = {}

    def __init__(self, base_path: Path):
        #
        # fill up the server types

        for module_info in pkgutil.iter_modules(['core/servers/types']):
            module = importlib.import_module(f"minecraft_manager.core.servers.types.{module_info.name}")
            for obj_name in dir(module):
                obj = getattr(module, obj_name)
                if isinstance(obj, type) and hasattr(obj, "name"):
                    self.SERVER_TYPES[obj.name] = obj()

        # set props
        self.base_path = base_path
        self.downloads = self.base_path / "downloads"
        self.servers = self.base_path / "servers"
        self.templates = self.base_path / "templates"


    def install(self, name: str, server_type: str, version: str, memory: str, eula: bool, first_start: bool):
        if server_type not in self.SERVER_TYPES:
            raise InvalidCliArgument(f"Unsupported server type: {server_type}")

        impl = self.SERVER_TYPES[server_type]

        target_dir = self.servers / name
        target_dir.mkdir(parents=True, exist_ok=True)

        if server_type == "fabric":
            impl.setup(self.downloads, version, java_path="java", dest_dir=target_dir)
        else:
            jar_path = self._download_jar(impl, version)
            shutil.copy(jar_path, target_dir / "server.jar")

        # copy templates and update eula
        for template in self.templates.glob("*"):
            shutil.copy(template, target_dir / template.name)
        if eula:
            (target_dir / "eula.txt").write_text("eula=true\n")

        # keep metadata
        meta = {
            "name": name,
            "type": server_type,
            "version": version,
            "memory": memory,
            "jar": str(target_dir / "server.jar"),
        }
        with open(target_dir / "mcman.yaml", "w") as f:
            yaml.dump(meta, f)

        print(f"Server installed at {target_dir}")

        if first_start:
            self._initialise_server(target_dir, memory)
        else:
            print("Skipping server start (--first-start).")

    def _initialise_server(self, target_dir: Path, memory: str):
        print("Starting server for initial setup...")
        try:
            proc = subprocess.Popen(
                ["java", f"-Xmx{memory}", "-jar", "server.jar", "nogui"],
                cwd=target_dir,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            # Wait till it generates files
            time.sleep(10)
            proc.stdin.write("stop\n")
            proc.stdin.flush()
            proc.wait(timeout=30)
            print("Server initialised successfully")
        except Exception as e:
            print(f"Server initialisation failed: {e}")

    def _download_jar(self, impl, version: str) -> Path:
        dest_path = self.downloads / impl.get_file_name(version)
        if dest_path.exists():
            print(f"Using cached {dest_path}")
            return dest_path

        print(f"Downloading {impl.name} {version}...")

        download_url = impl.get_download_url(version)
        r = requests.get(download_url, stream=True)
        r.raise_for_status()

        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Saved to {dest_path}")
        return dest_path
