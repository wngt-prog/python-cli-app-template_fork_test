import typer

app = typer.Typer()


@app.command()
def hello(name: str) -> None:
    """指定された名前で挨拶を表示する"""
    print(f"hello {name}")


@app.callback()
def main() -> None:
    """my-app CLI アプリケーション"""


if __name__ == "__main__":
    app()
