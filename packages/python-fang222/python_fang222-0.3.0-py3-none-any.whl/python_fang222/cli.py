"""Console script for python_fang222."""
import python_fang222

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for python_fang222."""
    console.print("Replace this message by putting your code into "
               "python_fang222.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
