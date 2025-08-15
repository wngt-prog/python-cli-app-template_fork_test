# Workflow

## 基本的なワークフロー

`docs/CONTRIBUTING.md` を参照してください。

## タスク開始

- タスクを開始する前に、あなたが守るべきルールを確認してください
- タスクを開始する際は、その計画とブランチ名をユーザーに提示して、ユーザーに確認をとってください

## Issue開始時の必須手順

**GitHubのissueを始める時は、必ず最初に専用のブランチを作成すること！**

```bash
git fetch
# Issue番号に対応したブランチ名で作成
# 例: Issue #1の場合
git switch -c feature/issue-1-project-setup origin/main

# または機能名を含める
git switch -c feature/issue-1-project-setup origin/main
```

## 作業の実行単位

タスクをひととおり終えて、`git add`, `git commit`, `git push`, `gh pr create` する段になったら作業を止めて、ユーザーに報告してください。

## 削除処理

ディレクトリやファイルを削除する際は、Git 管理されているか確認してください。

- Git 管理されている場合: `git rm` を使う
- Git 管理されていない場合: `rm` を使う
