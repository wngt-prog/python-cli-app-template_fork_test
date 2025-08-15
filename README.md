# Python Docker CLI App Template

`uv`とDockerを使用した、モダンなPython CLIアプリケーション開発のテンプレートプロジェクトです。

## 概要

このプロジェクトは、以下の技術スタックを使用してPython CLIアプリケーションを開発するためのベストプラクティスを示します：

- **🐍 Python 3.12**: 最新のPython機能を活用
- **⚡ uv**: 高速なPythonパッケージマネージャー（Rust製）
- **🐳 Docker & Docker Compose**: 一貫した開発環境
- **🔧 Typer**: モダンなCLIフレームワーク
- **✅ pytest**: 包括的なテストフレームワーク
- **🎨 ruff**: 高速なリンター・フォーマッター
- **🚀 GitHub Actions**: 自動化されたCI/CDパイプライン

## 特徴

- **🔒 完全に再現可能な環境**: `uv.lock`による厳密な依存関係管理
- **📦 最適化されたDockerイメージ**: マルチステージビルドとレイヤーキャッシュ
- **🔄 ライブリロード**: Docker Compose Watchによる開発効率向上
- **🛡️ 品質保証**: pre-commitフック、自動テスト、リンティング
- **📚 包括的なドキュメント**: セットアップから本番デプロイまで

## プロジェクト構成

```
python-docker-cli-app-template/
├── src/                      # Pythonソースコード
│   └── my_app/
│       ├── __init__.py
│       └── cli.py            # CLIエントリーポイント
├── tests/                    # テストコード
│   └── test_cli.py
├── .github/workflows/        # CI/CD設定 (GitHub Actions)
├── docs/                     # ドキュメント
├── .pre-commit-config.yaml   # pre-commitフック設定
├── Dockerfile                # 本番・開発兼用Dockerイメージ
├── compose.yml               # Docker Compose設定
├── pyproject.toml            # プロジェクト設定・依存関係
├── uv.lock                   # 依存関係ロックファイル
└── README.md                 # このファイル
```

## クイックスタート

詳細な手順は [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) を参照してください。

### 前提条件

- Docker & Docker Compose
- Git
- （推奨）pre-commit

### セットアップ

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/gnkm/python-docker-cli-app-template.git
   cd python-docker-cli-app-template
   ```

2. **Dockerイメージのビルドと依存関係の同期**
   ```bash
   docker compose build
   docker compose run --rm app uv sync
   ```

3. **Gitフックのセットアップ** (推奨)
   ```bash
   pre-commit install
   ```

### 使い方

#### CLIアプリケーションの実行

```bash
# ヘルプの表示
docker compose run --rm app my-app --help

# hello コマンドの実行
docker compose run --rm app my-app hello "World"
```

#### 開発モード (`watch`モード)

ソースコードの変更をコンテナに即時反映させるには、`watch`モードを使用します。

```bash
docker compose watch
```

## 本番デプロイ

### Dockerイメージのビルド

```bash
docker build -t my-app:latest .
```

### コンテナの実行

```bash
docker run --rm my-app:latest my-app hello "Production"
```

## 貢献

プロジェクトへの貢献を歓迎します！

開発環境のセットアップ、テストの実行方法、CI/CDパイプライン、開発ワークフローなどの詳細については、[`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) を参照してください。

## 技術的な詳細

### 採用技術の特徴

- **uv**: Rustで実装された高速なPythonパッケージマネージャー（pipの10-100倍高速）
- **Docker最適化**: マルチステージビルドとレイヤーキャッシュによる効率的なイメージ構築
- **品質保証**: 自動テスト、静的解析、継続的インテグレーションによる高品質なコード
