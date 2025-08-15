import importlib.metadata

import typer

__version__ = importlib.metadata.version("my-app")

app = typer.Typer()


def version_callback(value: bool) -> None:
    """バージョン情報を表示して終了する"""
    if value:
        print(f"my-app version: {__version__}")
        raise typer.Exit()


@app.command()
def hello(name: str) -> None:
    """指定された名前で挨拶を表示する"""
    print(f"hello {name}")


@app.command()
def version() -> None:
    """バージョン情報を表示する"""
    print(f"my-app version: {__version__}")


@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        help="バージョン情報を表示する",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """my-app CLI アプリケーション"""


if __name__ == "__main__":
    app()
