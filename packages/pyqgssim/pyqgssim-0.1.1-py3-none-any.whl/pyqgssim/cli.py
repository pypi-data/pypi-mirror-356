"""Console script for pyqgssim."""

import logging
import sys

import typer
from PySide2.QtWidgets import QApplication
from rich.console import Console
from rich.logging import RichHandler

from pyqgssim.gui.MainWindow import MainWindow

logging.basicConfig(
    level=logging.INFO,
    format="[*] %(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(markup=True)],
)

app = typer.Typer()
console = Console()


@app.command()
def cmd() -> None:
    """Console script for pyqgssim."""
    console.print(
        "Replace this message by putting your code into pyqgssim.cli.main",
    )
    console.print("See Typer documentation at https://typer.tiangolo.com/")


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
