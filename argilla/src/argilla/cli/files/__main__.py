"""Files CLI commands."""

from argilla.cli.typer_ext import ArgillaTyper

# Import all files CLI commands
from argilla.cli.files.list import list_files
from argilla.cli.files.upload import upload_file
from argilla.cli.files.download import download_file
from argilla.cli.files.delete import delete_file

app = ArgillaTyper(help="Manage files in workspaces", no_args_is_help=True)

# Register all commands
app.command(name="list")(list_files)
app.command(name="upload")(upload_file)
app.command(name="download")(download_file)
app.command(name="delete")(delete_file)

if __name__ == "__main__":
    app()
