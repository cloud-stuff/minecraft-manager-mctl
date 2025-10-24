from pathlib import Path
import typer

from mctl.core.initialiser import ProjectInitialiser

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
            "~/.mctl", "--path", "-p", help="Path where mctl will initialize its environment."
        ),
        force: bool = typer.Option(
            False, "--force", "-f", help="Override existing configs and directories if present."
        )
) -> None:
    """
    Initialise the mctl environment - create directory structure to store configs, servers, downloads, etc.
    """
    initialiser = ProjectInitialiser(path)

    try:
        result = initialiser.initialise(force)
    except FileExistsError as e:
        typer.echo(f"{e}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Initialisation failed: {e}")
        raise typer.Exit(code=1)

    for d in result.dirs:
        typer.echo(f"Created: {d}")

    typer.echo(f"Created config: {result.config_path}")
    typer.echo("Project structure successfully initialised")
