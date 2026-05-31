# クイックスタート

## クライアント作成

```python
from niconico import NicoNico

client = NicoNico()
```

## セッションでログイン

ログインが必要な API を使う場合は、`user_session` を渡します。

```python
from niconico import NicoNico

client = NicoNico()
client.login_with_session("user_session_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
```

!!! warning
    `user_session` は認証情報です。リポジトリ、Issue、ログ、CI 出力に含めないでください。

## CLI

```bash
niconico -h
```
