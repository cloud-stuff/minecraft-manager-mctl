from pathlib import Path
import yaml

from mctl.core.interfaces import InitialiserResponse

DEFAULT_DIRS = ["servers", "downloads", "templates", "logs"]
DEFAULT_CONFIG = {"java_path": "java", "memory": "2G"}

class ProjectInitialiser:

    def __init__(self, base: Path):
        self.base = base.expanduser().resolve()

    def initialise(self, force: bool) -> InitialiserResponse:
        if self.base.exists() and not force:
            raise FileExistsError(f"Directory {self.base} already exists.")

        for subdir in DEFAULT_DIRS:
            target = self.base / subdir
            target.mkdir(parents=True, exist_ok=True)

        config_path = self.base / "config.yaml"
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(DEFAULT_CONFIG, f)

        templates_dir = self.base / "templates"
        (templates_dir / "eula.txt").write_text("eula=true\n")

        return InitialiserResponse(
                base_path=str(self.base),
                dirs=[str(self.base / d) for d in DEFAULT_DIRS],
                config_path=str(config_path),
            )
