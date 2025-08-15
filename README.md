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
├── my-app/                     # メインアプリケーション
│   ├── src/my_app/            # Pythonソースコード
│   │   ├── __init__.py
│   │   └── cli.py             # CLIエントリーポイント
│   ├── tests/                 # テストコード
│   │   ├── __init__.py
│   │   └── test_cli.py
│   ├── Dockerfile             # 本番用Dockerイメージ
│   ├── compose.yml            # Docker Compose設定
│   ├── pyproject.toml         # プロジェクト設定・依存関係
│   └── uv.lock               # ロックファイル
├── docs/                      # ドキュメント
│   └── CONTRIBUTING.md        # 開発ガイド
├── .github/workflows/         # CI/CD設定
│   └── ci.yml                # GitHub Actions
└── README.md                  # このファイル
```

## クイックスタート

### 前提条件

- Docker & Docker Compose
- Git
- （オプション）pre-commit

### セットアップ

1. **リポジトリのクローン**
   ```bash
   git clone https://github.com/gnkm/python-docker-cli-app-template.git
   cd python-docker-cli-app-template/my-app
   ```

2. **Dockerイメージのビルド**
   ```bash
   docker compose build
   ```

3. **依存関係の同期**
   ```bash
   docker compose run --rm app uv sync
   ```

4. **Git フックのセットアップ**（推奨）
   ```bash
   # プロジェクトルートで実行
   cd ..
   pre-commit install
   ```

### 使い方

#### CLIアプリケーションの実行

```bash
# ヘルプの表示
docker compose run --rm app my-app --help

# hello コマンドの実行
docker compose run --rm app my-app hello "World"
docker compose run --rm app my-app hello "太郎"
```

#### 開発モード

Docker Compose Watchを使用してファイル変更を自動的に反映：

```bash
docker compose up --watch
```

## 開発

### テストの実行

```bash
# すべてのテストを実行
docker compose run --rm app pytest

# 詳細出力でテストを実行
docker compose run --rm app pytest -v

# 特定のテストファイルのみ実行
docker compose run --rm app pytest tests/test_cli.py
```

### コード品質チェック

```bash
# リンティング（自動修正付き）
docker compose run --rm app ruff check . --fix

# フォーマットチェック
docker compose run --rm app ruff format --check .

# フォーマット適用
docker compose run --rm app ruff format .
```

### 依存関係の管理

```bash
# 新しいパッケージの追加
docker compose run --rm app uv add <パッケージ名>

# 開発用パッケージの追加
docker compose run --rm app uv add <パッケージ名> --group dev

# 依存関係の更新
docker compose run --rm app uv lock
```

## CI/CD

このプロジェクトは GitHub Actions を使用した自動化されたCI/CDパイプラインを提供します。

### 自動実行されるチェック

- **プルリクエスト作成時**と**mainブランチへのプッシュ時**に自動実行
- ✅ **リンティング**: `ruff check`によるコード品質チェック
- ✅ **フォーマット**: `ruff format --check`によるコードスタイルチェック
- ✅ **テスト**: `pytest`による単体テスト・統合テスト
- ✅ **ビルド**: Dockerイメージのビルド確認

### ワークフロー設定

CI設定は `.github/workflows/ci.yml` で管理されています。

## 本番デプロイ

### Dockerイメージのビルド

```bash
cd my-app
docker build -t my-app:latest .
```

### コンテナの実行

```bash
docker run --rm my-app:latest my-app hello "Production"
```

## 貢献

プロジェクトへの貢献を歓迎します！詳細な開発ガイドラインについては、[`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) を参照してください。

### 開発ワークフロー

1. Issue の作成
2. フィーチャーブランチの作成
3. 開発・テスト
4. プルリクエストの作成
5. コードレビュー
6. マージ

## ライセンス

このプロジェクトは [MIT License](LICENSE) の下で公開されています。

## 技術的な詳細

### なぜ uv を使用するのか？

- **高速**: Rustで実装され、pipの10-100倍高速
- **信頼性**: 厳密な依存関係解決
- **互換性**: pip互換のAPIを提供
- **モダン**: 最新のPythonエコシステムに対応

### Docker最適化

- **マルチステージビルド**: 依存関係のインストールと最終イメージを分離
- **レイヤーキャッシュ**: 効率的な再ビルド
- **最小限のイメージサイズ**: 不要なファイルを除外

### 品質保証

- **型ヒント**: 型安全性の向上
- **自動テスト**: 包括的なテストカバレッジ
- **静的解析**: ruffによる高速なリンティング
- **継続的インテグレーション**: 自動化された品質チェック
