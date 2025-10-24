import typer

from mctl.core.servers.configurator import ServerConfigManager

app = typer.Typer()

@app.command("set")
def set_server_property(
        server_name: str = typer.Argument(
            ...,
            help="Name of the Minecraft server to update configuration for.",
            metavar="SERVER",
        ),
        key: str = typer.Argument(
            ...,
            help="Configuration key to modify (e.g., 'motd', 'online-mode').",
            metavar="KEY",
        ),
        value: str = typer.Argument(
            ...,
            help="New value to set for the given key.",
            metavar="VALUE",
        ),
    ) -> None:
    """Set a configuration value in server.properties."""
    try:
        cfg = ServerConfigManager(server_name)
        cfg.set(key, value)
        typer.echo(f"Updated '{key}' = '{value}' for '{server_name}'")
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1)


@app.command("get")
def get_server_property(
        server_name: str = typer.Argument(
            ...,
            help="Name of the Minecraft server to read configuration from.",
            metavar="SERVER",
        ),
        key: str = typer.Argument(
            ...,
            help="Configuration key to retrieve (e.g., 'motd', 'max-players').",
            metavar="KEY",
        ),
    ) -> None:
    """Get a configuration value from server.properties."""
    try:
        cfg = ServerConfigManager(server_name)
        value = cfg.get(key)
        if value is None:
            typer.echo(f"Key '{key}' not found in '{server_name}'.")
        else:
            typer.echo(value)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(1)
