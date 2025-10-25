import pkgutil
import importlib
import shutil
import subprocess
import time
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, cast, Optional

import requests
import yaml

from mctl.core.exceptions import InvalidCliArgument
from mctl.core.servers.types.base import BaseInstaller
from mctl.core.servers.types.fabric import FabricInstaller


@dataclass
class InstallArguments:
    name: str
    server_type: str
    version: str
    memory: str
    eula: bool
    first_start: bool

class ServerInstaller:

    SERVER_TYPES: Dict[str, BaseInstaller] = {}

    def __init__(self, base_path: Path):
        #
        # fill up the server types

        types_dir = (Path(__file__).parent / "types").resolve()
        for module_info in pkgutil.iter_modules([str(types_dir)]):
            module = importlib.import_module(f"mctl.core.servers.types.{module_info.name}")
            for obj_name in dir(module):
                obj = getattr(module, obj_name)
                if isinstance(obj, type) and hasattr(obj, "name"):
                    self.SERVER_TYPES[obj.name] = obj()

        # set props
        self.base_path = base_path
        self.downloads = self.base_path / "downloads"
        self.servers = self.base_path / "servers"
        self.templates = self.base_path / "templates"


    def install(self, args: InstallArguments) -> None:
        if args.server_type not in self.SERVER_TYPES:
            raise InvalidCliArgument(f"Unsupported server type: {args.server_type}")

        impl = self.SERVER_TYPES[args.server_type]

        target_dir = self.servers / args.name
        target_dir.mkdir(parents=True, exist_ok=True)

        if args.server_type == "fabric":
            impl = cast(FabricInstaller, impl)
            impl.setup(self.downloads, args.version, java_path="java", dest_dir=target_dir)
        else:
            jar_path = self._download_jar(impl, args.version)
            shutil.copy(jar_path, target_dir / "server.jar") # type: ignore

        # copy templates and update eula
        for template in self.templates.glob("*"):
            shutil.copy(template, target_dir / template.name)
        if args.eula:
            (target_dir / "eula.txt").write_text("eula=true\n")

        # keep metadata
        meta = {
            "name": args.name,
            "type": args.server_type,
            "version": args.version,
            "memory": args.memory,
            "jar": str(target_dir / "server.jar"),
        }
        with open(target_dir / "mctl.yaml", "w", encoding="utf-8") as f:
            yaml.dump(meta, f)

        print(f"Server installed at {target_dir}")

        if args.first_start:
            self._initialise_server(target_dir, args.memory)
        else:
            print("Skipping server start (--first-start).")

    def _initialise_server(self, target_dir: Path, memory: str) -> None:
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
            if proc.stdin is not None:
                proc.stdin.write("stop\n")
                proc.stdin.flush()
                proc.wait(timeout=30)
            print("Server initialised successfully")
        except Exception as e:
            print(f"Server initialisation failed: {e}")

    def _download_jar(self, impl: BaseInstaller, version: str) -> Optional[Path]:
        dest_path = self.downloads / impl.get_file_name(version)
        if dest_path.exists():
            print(f"Using cached {dest_path}")
            return dest_path

        print(f"Downloading {impl.name} {version}...")

        download_url = impl.get_download_url(version)
        r = requests.get(download_url, stream=True, timeout=120)
        r.raise_for_status()

        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Saved to {dest_path}")
        return dest_path
