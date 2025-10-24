from pathlib import Path
import typer
import yaml

app = typer.Typer()

DEFAULT_DIRS = ["servers", "downloads", "templates", "backups"]

DEFAULT_CONFIG = {
    "java_path": "java",
    "default_memory": "2G",
    "default_server_type": "paper",
    "default_version": "latest",
    "rcon_port_start": 25575,
    "servers_root": "servers",
    "downloads_root": "downloads",
    "backups_root": "backups",
    "templates_root": "templates",
}


@app.command()
def init(
        path: Path = typer.Option(
            "~/.mcman", "--path", "-p", help="Path where mcman will initialize its environment."
        ),
        force: bool = typer.Option(
            False, "--force", "-f", help="Override existing configs and directories if present."
        )
) -> None:
    """
    Initialise the mcman environment - create directory structure to store configs, servers, downloads, etc.
    """
    base = Path(path).expanduser().resolve()

    if base.exists() and not force:
        typer.echo(f"Directory {base} already exists. Use --force to override or enter other directory.")
        raise typer.Exit(code=1)

    for subdir in DEFAULT_DIRS:
        target = base / subdir
        target.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Created: {target}")

    config_path = base / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(DEFAULT_CONFIG, f)
    typer.echo(f"Created config: {config_path}")

    templates_dir = base / "templates"
    (templates_dir / "eula.txt").write_text("eula=true\n")

    typer.echo(f"mcman environment successfully initialised at: {base}")
