import re
import typer

def validate_arg_alphanumeric(name: str) -> str:
    """
    Allows only letters, numbers, and dashes.
    """
    if not re.match(r"^[A-Za-z0-9-]+$", name):
        raise typer.BadParameter(
            "This argument can contain only letters, numbers, or dashes (e.g., survival-1, myserver)."
        )
    return name
