# 開発

## セットアップ

このプロジェクトは uv を利用します。

```bash
uv sync --locked --all-groups
```

## テスト

```bash
uv run pytest
```

## 静的チェック

```bash
uv run ruff check .
uv run pyright
```

## ドキュメント

```bash
uv run mkdocs serve
```

ビルド確認は次のコマンドで行います。

```bash
uv run mkdocs build --strict
```
