"""
CLIアプリケーションのテスト
"""

from typer.testing import CliRunner

from my_app.cli import app

runner = CliRunner()


def test_hello_command():
    """helloコマンドが正しく動作することをテスト"""
    result = runner.invoke(app, ["hello", "World"])
    assert result.exit_code == 0
    assert "hello World" in result.stdout


def test_hello_command_with_japanese():
    """helloコマンドが日本語の名前でも正しく動作することをテスト"""
    result = runner.invoke(app, ["hello", "太郎"])
    assert result.exit_code == 0
    assert "hello 太郎" in result.stdout


def test_main_help():
    """メインアプリケーションのヘルプが表示されることをテスト"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "my-app CLI アプリケーション" in result.stdout
    assert "hello" in result.stdout


def test_hello_help():
    """helloコマンドのヘルプが表示されることをテスト"""
    result = runner.invoke(app, ["hello", "--help"])
    assert result.exit_code == 0
    assert "指定された名前で挨拶を表示する" in result.stdout


def test_hello_without_argument():
    """helloコマンドに引数がない場合エラーになることをテスト"""
    result = runner.invoke(app, ["hello"])
    assert result.exit_code != 0
    # Typerのエラーメッセージは通常stderrに出力される
    assert "Missing argument" in result.stderr or result.exit_code == 2
