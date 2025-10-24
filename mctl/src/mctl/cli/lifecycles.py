import typer

from mctl.core.servers.manager import ServerManager
from mctl.core.utils.validators import validate_arg_alphanumeric

app = typer.Typer()

@app.command()
def start(
        name: str = typer.Argument(
            ...,
            help="Name of the server instance.",
            callback=validate_arg_alphanumeric,
        ),
    ) -> None:
    typer.echo(f"Starting server '{name}'")
    ServerManager(name).start()

@app.command()
def stop(
        name: str = typer.Argument(
            ...,
            help="Name of the server instance.",
            callback=validate_arg_alphanumeric,
        ),
    ) -> None:
    typer.echo(f"Stopping server '{name}'")
    ServerManager(name).stop()
