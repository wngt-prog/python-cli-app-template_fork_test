# Contributing Guide

## 開発の進め方

このプロジェクトの開発はDockerコンテナ内で行います。`docker compose` を通じて、環境の構築からコマンドの実行までを行います。

**重要な注意事項**:
- このプロジェクトでは `uv` の `pip` 互換インターフェース (`uv pip ...`) は使用しません
- **すべての `uv` コマンド（`uv sync`, `uv lock`, `uv add` など）は必ずDockerコンテナ内で実行してください**
- ホストマシンで直接 `uv` コマンドを実行すると、環境の不整合が発生する可能性があります

### 1. 初回セットアップ

まず、プロジェクトをローカルで開発できる状態に準備します。

1.  **Gitフックのセットアップ**

    コミット前に品質チェックを自動化するため、**ホストマシン（お使いのPC）**で`pre-commit`フックをインストールします。
    ```bash
    # pre-commitが未インストールの場合: pip install pre-commit
    pre-commit install
    ```

2.  **Dockerイメージのビルド**

    開発用のDockerイメージをビルドします。
    ```bash
    docker compose build
    ```

3.  **依存関係の同期**

    `uv.lock`ファイルに基づいて、コンテナ内に**完全に再現可能な**開発環境を構築します。このコマンドは、`pyproject.toml`で定義された全ての依存関係（開発用を含む）をインストールします。
    ```bash
    docker compose run --rm app uv sync
    ```
    *注意: `app`は`compose.yml`で定義するサービス名です。これは後続のタスクで作成します。*

### 日々の開発ワークフロー: `watch`モードの活用

初回セットアップ完了後の日常的な開発では、`docker compose watch`コマンドの使用を強く推奨します。これにより、開発サイクルが大幅に効率化されます。

```bash
# プロジェクトのルートディレクトリ（my-app/）で実行
docker compose watch
```

`watch`モードを有効にすると、`compose.yml`の`develop.watch`セクションで定義されたルールに基づき、以下の機能が自動的に有効になります。

1.  **ソースコードの自動同期**:
    ローカルでソースコードファイル（`.py`など）を変更して保存すると、その内容が**コンテナを再起動することなく即座に**反映されます。これにより、修正と動作確認を素早く繰り返すことができます。

2.  **依存関係変更時の自動リビルド**:
    `pyproject.toml`や`uv.lock`ファイルが変更されると、Docker Composeがそれを検知し、**自動でDockerイメージを再ビルド**します。これにより、`uv add`などで新しいライブラリを追加した後に、手動で`docker compose build`を実行する手間が省けます。

テストの実行やリンターの適用など、個別のコマンドを実行したい場合は、`watch`モードを起動しているターミナルとは**別のターミナル**を開き、従来通り`docker compose run --rm app <コマンド>`を実行してください。

### 2. 依存関係の追加・更新

新しいパッケージを追加したい場合は、以下のコマンドを使用します。

```bash
# 通常の依存関係として追加
docker compose run --rm app uv add <パッケージ名>

# 開発用の依存関係として追加 (例: pytest)
docker compose run --rm app uv add pytest --group dev
```

このコマンドを実行すると、`pyproject.toml`と`uv.lock`が自動的に更新されます。更新されたこれらのファイルは、必ずGitにコミットしてください。

**依存関係に関する重要な注意**:
- `pyproject.toml`を手動で編集した場合は、必ず `docker compose run --rm app uv lock` を実行してロックファイルを更新してください
- ロックファイルの更新後は、`docker compose build` でDockerイメージを再ビルドする必要があります

### 3. テストの実行

コードの品質を保つため、変更を行った際は必ずテストを実行してください。

```bash
# すべてのテストを実行
docker compose run --rm app pytest

# 詳細な出力でテストを実行
docker compose run --rm app pytest -v

# 特定のテストファイルのみを実行
docker compose run --rm app pytest tests/test_cli.py

# 特定のテスト関数のみを実行
docker compose run --rm app pytest tests/test_cli.py::test_hello_command
```

### 4. コード品質チェック

コードの品質を保つため、`ruff`によるリンティングとフォーマットチェックを実行してください。

```bash
# リンティング実行（エラーがあれば自動修正）
docker compose run --rm app ruff check . --fix

# フォーマットチェック
docker compose run --rm app ruff format --check .

# フォーマット適用
docker compose run --rm app ruff format .
```

### 5. 継続的インテグレーション (CI)

このプロジェクトでは、GitHub Actionsを使用してCI/CDパイプラインが設定されています。

**自動実行されるチェック**:
- プルリクエスト作成時とmainブランチへのプッシュ時に自動実行
- `ruff`によるリンティングとフォーマットチェック
- `pytest`によるテスト実行
- Dockerイメージのビルド確認

**ローカルでの事前チェック**:
プルリクエストを作成する前に、ローカルで以下のコマンドを実行してCIが成功することを確認してください：

```bash
cd my-app

# 1. リンティングチェック
docker compose run --rm app ruff check . --fix

# 2. フォーマットチェック
docker compose run --rm app ruff format --check .

# 3. テスト実行
docker compose run --rm app pytest -v

# 4. Dockerビルド確認
docker compose build
```
