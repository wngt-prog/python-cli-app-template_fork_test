# Dockerでuvを使用する

## はじめに

> **ヒント**
> Dockerでアプリケーションをビルドする際にuvを使用するためのベストプラクティスについては、[`uv-docker-example`](https://github.com/astral-sh/uv-docker-example)プロジェクトの例を参照してください。

uvは、*distroless*なDockerイメージと、一般的なベースイメージから派生したイメージの両方を提供しています。distrolessイメージは、独自のイメージビルドに[uvバイナリをコピーする](https://docs.astral.sh/uv/guides/integration/docker/#installing-uv)のに役立ちます。一方、派生イメージは、コンテナ内でuvを使用するのに便利です。distrolessイメージにはuvバイナリ以外は何も含まれていませんが、派生イメージにはuvがプリインストールされたオペレーティングシステムが含まれています。

例として、Debianベースのイメージを使用してコンテナ内でuvを実行するには、次のようにします。

```shell
$ docker run --rm -it ghcr.io/astral-sh/uv:debian uv --help
```

### 利用可能なイメージ

以下のdistrolessイメージが利用可能です：

  * `ghcr.io/astral-sh/uv:latest`
  * `ghcr.io/astral-sh/uv:{major}.{minor}.{patch}` (例: `ghcr.io/astral-sh/uv:0.8.7`)
  * `ghcr.io/astral-sh/uv:{major}.{minor}` (例: `ghcr.io/astral-sh/uv:0.8`、最新のパッチバージョン)

そして、以下の派生イメージが利用可能です：

  * `alpine:3.21` ベース:
      * `ghcr.io/astral-sh/uv:alpine`
      * `ghcr.io/astral-sh/uv:alpine3.21`
  * `debian:bookworm-slim` ベース:
      * `ghcr.io/astral-sh/uv:debian-slim`
      * `ghcr.io/astral-sh/uv:bookworm-slim`
  * `buildpack-deps:bookworm` ベース:
      * `ghcr.io/astral-sh/uv:debian`
      * `ghcr.io/astral-sh/uv:bookworm`
  * `python3.x-alpine` ベース:
      * `ghcr.io/astral-sh/uv:python3.14-rc-alpine`
      * `ghcr.io/astral-sh/uv:python3.13-alpine`
      * ... (python3.8まで)
  * `python3.x-bookworm` ベース:
      * `ghcr.io/astral-sh/uv:python3.14-rc-bookworm`
      * `ghcr.io/astral-sh/uv:python3.13-bookworm`
      * ... (python3.8まで)
  * `python3.x-slim-bookworm` ベース:
      * `ghcr.io/astral-sh/uv:python3.14-rc-bookworm-slim`
      * `ghcr.io/astral-sh/uv:python3.13-bookworm-slim`
      * ... (python3.8まで)

distrolessイメージと同様に、各派生イメージは `ghcr.io/astral-sh/uv:{major}.{minor}.{patch}-{base}` や `ghcr.io/astral-sh/uv:{major}.{minor}-{base}` のようなuvバージョンタグ付きで公開されます (例: `ghcr.io/astral-sh/uv:0.8.7-alpine`)。

さらに、`0.8` 以降、各派生イメージでは `UV_TOOL_BIN_DIR` が `/usr/local/bin` に設定されており、デフォルトユーザーで `uv tool install` が期待通りに動作するようになっています。

詳細については、[GitHub Container](https://github.com/astral-sh/uv/pkgs/container/uv)ページをご覧ください。

### Installing uv

uvがプリインストールされた上記のイメージのいずれかを使用するか、公式のdistroless Dockerイメージからバイナリをコピーしてuvをインストールします：

```dockerfile
# Dockerfile
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```

または、インストーラーを使用します：

```dockerfile
# Dockerfile
FROM python:3.12-slim-bookworm

# インストーラーはリリースアーカイブをダウンロードするためにcurl（と証明書）が必要です
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# 最新のインストーラーをダウンロード
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# インストーラーを実行してから削除
RUN sh /uv-installer.sh && rm /uv-installer.sh

# インストールされたバイナリが`PATH`上にあることを確認
ENV PATH="/root/.local/bin/:$PATH"
```

この方法では `curl` が利用可能である必要があります。

どちらの場合でも、特定のuvバージョンに固定することがベストプラクティスです。例：

```dockerfile
COPY --from=ghcr.io/astral-sh/uv:0.8.7 /uv /uvx /bin/
```

> **ヒント**
> 上記のDockerfileの例では特定のタグに固定していますが、特定のSHA256に固定することも可能です。再現性のあるビルドが求められる環境では、タグは異なるコミットSHAに移動する可能性があるため、特定のSHA256に固定することがベストプラクティスとされています。
>
> ```dockerfile
> # 例：以前のリリースのハッシュを使用
> COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/
> ```

または、インストーラーを使用する場合：

```dockerfile
ADD https://astral.sh/uv/0.8.7/install.sh /uv-installer.sh
```

### プロジェクトのインストール

プロジェクト管理にuvを使用している場合は、プロジェクトをイメージにコピーしてインストールできます：

```dockerfile
# Dockerfile

# プロジェクトをイメージにコピー
ADD . /app

# プロジェクトを新しい環境に同期し、ロックファイルが最新であることを確認
WORKDIR /app
RUN uv sync --locked
```

> **重要**
> リポジトリに[`.dockerignore`ファイル](https://docs.docker.com/build/concepts/context/#dockerignore-files)を作成し、`.venv`を追加してイメージビルドに含まれないようにすることがベストプラクティスです。プロジェクトの仮想環境はローカルのプラットフォームに依存するため、イメージ内ではゼロから作成する必要があります。

そして、デフォルトでアプリケーションを起動するには：

```dockerfile
# Dockerfile

# プロジェクトによって提供される`my_app`コマンドがあると仮定
CMD ["uv", "run", "my_app"]
```

> **ヒント**
> Dockerイメージのビルド時間を改善するために、依存関係のインストールとプロジェクト自体のインストールを分離する[中間レイヤー](https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers)を使用することがベストプラクティスです。

完全な例は、[`uv-docker-example`プロジェクト](https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile)で確認できます。

### 環境の使用

プロジェクトをインストールしたら、プロジェクトの仮想環境のバイナリディレクトリをパスの先頭に置くことで、環境を*アクティベート*できます：

```dockerfile
# Dockerfile
ENV PATH="/app/.venv/bin:$PATH"
```

または、環境が必要なコマンドには `uv run` を使用することもできます：

```dockerfile
# Dockerfile
RUN uv run some_script.py
```

> **ヒント**
> 代わりに、[`UV_PROJECT_ENVIRONMENT`設定](https://docs.astral.sh/uv/concepts/projects/config/#project-environment-path)を同期前に設定することで、システムのPython環境にインストールし、環境のアクティベーションを完全にスキップすることもできます。

### インストールされたツールの使用

インストールされたツールを使用するには、[ツールのbinディレクトリ](https://docs.astral.sh/uv/concepts/tools/#the-bin-directory)がパス上にあることを確認してください：

```dockerfile
# Dockerfile
ENV PATH=/root/.local/bin:$PATH
RUN uv tool install cowsay
```

```shell
$ docker run -it $(docker build -q .) /bin/bash -c "cowsay -t hello"
  _____
| hello |
  =====
     \
      \
        ^__^
        (oo)\_______
        (__)\       )\/\
            ||----w |
            ||     ||
```

> **注意**
> ツールのbinディレクトリの場所は、コンテナ内で `uv tool dir --bin` コマンドを実行することで確認できます。
>
> また、特定の場所に設定することも可能です：
>
> ```dockerfile
> # Dockerfile
> ENV UV_TOOL_BIN_DIR=/opt/uv-bin/
> ```

### ARM muslイメージへのPythonのインストール

uvは、イメージ内に互換性のあるPythonバージョンがない場合、[それをインストールしようとします](https://docs.astral.sh/uv/guides/install-python/)が、ARM上のmusl Linux向けのPythonインストールはまだサポートしていません。例えば、ARMマシン上でAlpine Linuxベースイメージを使用している場合、システムのパッケージマネージャで追加する必要があるかもしれません：

```shell
apk add --no-cache python3~=3.12
```

## コンテナでの開発

開発時には、プロジェクトディレクトリをコンテナにマウントすると便利です。この設定により、プロジェクトへの変更がイメージを再ビルドすることなく、コンテナ化されたサービスに即座に反映されます。ただし、プロジェクトの仮想環境（`.venv`）をマウントに含め*ない*ことが重要です。なぜなら、仮想環境はプラットフォームに特化しており、イメージ用にビルドされたものを使用するべきだからです。

### `docker run`でのプロジェクトのマウント

作業ディレクトリのプロジェクトを`/app`にバインドマウントしつつ、`.venv`ディレクトリは[匿名ボリューム](https://docs.docker.com/engine/storage/#volumes)で保持します：

```shell
$ docker run --rm --volume .:/app --volume /app/.venv [...]
```

> **ヒント**
> `--rm` フラグは、コンテナが終了したときにコンテナと匿名ボリュームがクリーンアップされることを保証するために含まれています。

完全な例は、[`uv-docker-example`プロジェクト](https://github.com/astral-sh/uv-docker-example/blob/main/run.sh)で確認できます。

### `docker compose`での`watch`の設定

Docker Composeを使用する場合、コンテナ開発のためにより高度なツールが利用できます。[ `watch` ](https://docs.docker.com/compose/file-watch/#compose-watch-versus-bind-mounts)オプションを使用すると、バインドマウントよりも細やかな制御が可能になり、ファイルが変更されたときにコンテナ化されたサービスの更新をトリガーすることができます。

> **注意**
> この機能にはCompose 2.22.0が必要で、これはDocker Desktop 4.24にバンドルされています。

[Docker Composeファイル](https://docs.docker.com/compose/compose-application-model/#the-compose-file)で `watch` を設定して、プロジェクトの仮想環境を同期せずにプロジェクトディレクトリをマウントし、設定が変更されたときにイメージを再ビルドするようにします：

```yaml
# compose.yaml
services:
  example:
    build: .

    # ...

    develop:
      # アプリを更新するための`watch`設定を作成
      watch:
        # 作業ディレクトリをコンテナの`/app`ディレクトリと同期
        - action: sync
          path: .
          target: /app
          # プロジェクトの仮想環境を除外
          ignore:
            - .venv/

        # `pyproject.toml`の変更時にイメージを再ビルド
        - action: rebuild
          path: ./pyproject.toml
```

その後、`docker compose watch` を実行して、開発設定でコンテナを実行します。

完全な例は、[`uv-docker-example`プロジェクト](https://github.com/astral-sh/uv-docker-example/blob/main/compose.yml)で確認できます。

## 最適化

### バイトコードのコンパイル

Pythonソースファイルをバイトコードにコンパイルすることは、起動時間を改善する傾向があるため、本番イメージでは一般的に望ましいです（インストール時間は長くなります）。

バイトコードのコンパイルを有効にするには、`--compile-bytecode` フラグを使用します：

```dockerfile
# Dockerfile
RUN uv sync --compile-bytecode
```

または、`UV_COMPILE_BYTECODE` 環境変数を設定して、Dockerfile内のすべてのコマンドがバイトコードをコンパイルするようにすることもできます：

```dockerfile
# Dockerfile
ENV UV_COMPILE_BYTECODE=1
```

### キャッシング

ビルド間のパフォーマンスを向上させるために、[キャッシュマウント](https://docs.docker.com/build/guide/mounts/#add-a-cache-mount)を使用できます：

```dockerfile
# Dockerfile
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
```

デフォルトの [`UV_LINK_MODE`](https://docs.astral.sh/uv/reference/settings/#link-mode) を変更すると、キャッシュと同期先が別々のファイルシステム上にあるためハードリンクが使用できないという警告が表示されなくなります。

キャッシュをマウントしない場合は、`--no-cache` フラグを使用するか `UV_NO_CACHE` を設定することでイメージサイズを削減できます。

> **注意**
> キャッシュディレクトリの場所は、コンテナ内で `uv cache dir` コマンドを実行することで確認できます。
>
> また、キャッシュを特定の場所に設定することも可能です：
>
> ```dockerfile
> # Dockerfile
> ENV UV_CACHE_DIR=/opt/uv-cache/
> ```

### 中間レイヤー

プロジェクト管理にuvを使用している場合、`--no-install` オプションを使用して、推移的な依存関係のインストールを独自のレイヤーに移動することで、ビルド時間を改善できます。

`uv sync --no-install-project` は、プロジェクトの依存関係をインストールしますが、プロジェクト自体はインストールしません。プロジェクトは頻繁に変更されますが、その依存関係は一般的に静的であるため、これは大きな時間節約になります。

```dockerfile
# Dockerfile

# uvをインストール
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 作業ディレクトリを`app`ディレクトリに変更
WORKDIR /app

# 依存関係をインストール
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# プロジェクトをイメージにコピー
ADD . /app

# プロジェクトを同期
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
```

プロジェクトのルートと名前を識別するために `pyproject.toml` が必要ですが、プロジェクトの*内容*は最後の `uv sync` コマンドまでイメージにコピーされないことに注意してください。

> **ヒント**
> [ワークスペース](https://docs.astral.sh/uv/concepts/projects/workspaces/)を使用している場合は、プロジェクト*および*すべてのワークスペースメンバーを除外する `--no-install-workspace` フラグを使用してください。
>
> 特定のパッケージを同期から除外したい場合は、`--no-install-package <name>` を使用してください。

### 非編集可能インストール

デフォルトでは、uvはプロジェクトとワークスペースメンバーを編集可能モードでインストールし、ソースコードの変更が環境に即座に反映されるようにします。

`uv sync` と `uv run` は両方とも `--no-editable` フラグを受け付けます。これは、プロジェクトを非編集可能モードでインストールし、ソースコードへの依存をなくすようにuvに指示します。

マルチステージのDockerイメージの文脈では、`--no-editable` を使用して、あるステージで同期された仮想環境にプロジェクトを含め、その後、仮想環境だけを（ソースコードではなく）最終イメージにコピーすることができます。

例：

```dockerfile
# Dockerfile

# uvをインストール
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 作業ディレクトリを`app`ディレクトリに変更
WORKDIR /app

# 依存関係をインストール
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# プロジェクトを中間イメージにコピー
ADD . /app

# プロジェクトを同期
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

FROM python:3.12-slim

# ソースコードではなく、環境をコピー
COPY --from=builder --chown=app:app /app/.venv /app/.venv

# アプリケーションを実行
CMD ["/app/.venv/bin/hello"]
```

### uvの一時的な使用

最終イメージにuvが不要な場合、各呼び出しでバイナリをマウントすることができます：

```dockerfile
# Dockerfile
RUN --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
    uv sync
```

## イメージの来歴検証

Dockerイメージは、その出所を証明するためにビルドプロセス中に署名されます。これらの証明書（attestations）を使用して、イメージが公式チャネルから生成されたものであることを確認できます。

例えば、[GitHub CLIツール `gh`](https://cli.github.com/) を使用して証明書を検証できます：

```shell
$ gh attestation verify --owner astral-sh oci://ghcr.io/astral-sh/uv:latest
Loaded digest sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx for oci://ghcr.io/astral-sh/uv:latest
Loaded 1 attestation from GitHub API

The following policy criteria will be enforced:
- OIDC Issuer must match:................... https://token.actions.githubusercontent.com
- Source Repository Owner URI must match:... https://github.com/astral-sh
- Predicate type must match:................ https://slsa.dev/provenance/v1
- Subject Alternative Name must match regex: (?i)^https://github.com/astral-sh/

✓ Verification succeeded!

sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx was attested by:
REPO          PREDICATE_TYPE                  WORKFLOW
astral-sh/uv  https://slsa.dev/provenance/v1  .github/workflows/build-docker.yml@refs/heads/main
```

これは、特定のDockerイメージが公式のuv GitHubリリースワークフローによってビルドされ、その後改ざんされていないことを示しています。

GitHubの証明書は [sigstore.dev](https://www.sigstore.dev/) インフラストラクチャ上に構築されています。そのため、[`cosign`](https://github.com/sigstore/cosign) コマンドを使用して、`uv` の（マルチプラットフォーム）マニフェストに対する証明書BLOBを検証することもできます。

> **ヒント**
> これらの例では `latest` を使用していますが、ベストプラクティスは、特定のバージョンタグ（例：`ghcr.io/astral-sh/uv:0.8.7`）や、さらに良いのは特定のイメージダイジェスト（例：`ghcr.io/astral-sh/uv:0.5.27@sha256:5adf...`）に対する証明書を検証することです。

## 引用

[Using uv in Docker | uv](https://docs.astral.sh/uv/guides/integration/docker/)