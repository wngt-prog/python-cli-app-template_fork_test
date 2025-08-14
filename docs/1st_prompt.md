# Python Sample App(my-app)

## 概要

uv と Docker Compose を使った簡単な CLI アプリケーションを作る

## 使用方法

my-app の help を表示する。

```
docker compose run my-app
```

"hello ${name}" と表示させる。

```
docker compose run my-app hello ${name}
```

## 技術スタック

- Python(Docker)
- uv
- Typer

## 参考

`docs/using-uv-in-docker.md`、`uv-docker-example-main` を参考に適切な開発フローを定めること。
