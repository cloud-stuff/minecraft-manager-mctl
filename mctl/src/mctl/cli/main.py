import os
import typer
from mctl.cli import lifecycles, init, servers, config

os.environ["NO_COLOR"] = "1"

app = typer.Typer(help="Minecraft Server Manager CLI", pretty_exceptions_enable=False, rich_markup_mode=None)
app.add_typer(init.app)
app.add_typer(servers.app, name="server")
app.add_typer(lifecycles.app)
app.add_typer(config.app, name="config")

def main():
    app()

if __name__ == '__main__':
    app()
