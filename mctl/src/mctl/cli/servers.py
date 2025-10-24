import typer

from mctl.core.constants import DEFAULT_HOME_PATH
from mctl.core.servers.installer import ServerInstaller
from mctl.core.servers.registry import ServerRegistry
from mctl.core.utils.validators import validate_arg_alphanumeric

app = typer.Typer(help="Server tools: install new server, remove it, print server info")

@app.command()
def install(
        name: str = typer.Argument(
            ...,
            help="Name of the server instance.",
            callback=validate_arg_alphanumeric,
        ),

        server_type: str = typer.Option(
            "vanilla",
            "--type",
            "-t",
            help="Type of server software to install.",
            case_sensitive=False,
            show_choices=True,
            rich_help_panel="Server type",
            metavar="TYPE"
        ),

        version: str = typer.Option(
            "latest",
            "--version",
            "-v",
            help="Minecraft version (e.g., 1.21.1). Use 'latest' for newest version."
        ),

        memory: str = typer.Option(
            "2G",
            "--memory",
            "-m",
            help="Maximum server memory allocation."
        ),

        eula: bool = typer.Option(
            False,
            "--eula-accept",
            help="Accept Mojang's EULA."
        ),

        first_start: bool = typer.Option(
            False,
            "--first-start",
            help="Optional first start to generate world and configs and gracefully exit."
        ),
    ):
    typer.echo(f"Installing server: {server_type} {version}")

    try:
        ServerInstaller(DEFAULT_HOME_PATH).install(name.lower(), server_type, version, memory, eula, first_start)
    except Exception as e:
        typer.echo(str(e))
        raise typer.Exit(code=1)


@app.command()
def remove(
        name: str = typer.Argument(
            ...,
            help="Name of the server instance.",
            callback=validate_arg_alphanumeric,
        ),
    ):
    server_registry = ServerRegistry(DEFAULT_HOME_PATH.resolve())

    try:
        server_registry.remove(name)
    except FileNotFoundError:
        typer.echo("Project not found - nothing to delete.")
        raise typer.Exit(code=0)
    except Exception as e:
        typer.echo(f"Unexpected error while reading server info: {e}")
        raise typer.Exit(code=1)

    typer.echo(f"Server '{name}' removed successfully.")


@app.command()
def info(
        name: str = typer.Argument(
            ...,
            help="Name of the server instance.",
            callback=validate_arg_alphanumeric,
        ),
    ):
    server_registry = ServerRegistry(DEFAULT_HOME_PATH.resolve())

    try:
        server_info = server_registry.get_info(name)
    except FileNotFoundError:
        typer.echo("Project configuration file does not exist.")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error while reading server info: {e}")
        raise typer.Exit(code=1)

    typer.echo(f"\n📋  Info for server '{name}':")
    typer.echo(f"   Path:      {server_info.path}")
    typer.echo(f"   Type:      {server_info.type}")
    typer.echo(f"   Version:   {server_info.version}")
    typer.echo(f"   Memory:    {server_info.memory}")
    typer.echo(f"   Jar:       {server_info.jar}")
    typer.echo(f"   Java:      {server_info.java}")
    typer.echo("")
