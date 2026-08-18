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

セッション文字列が手元に無い場合は、ブラウザでログイン済みのセッションをそのまま取り込めます。

```python
from niconico import NicoNico

client = NicoNico()
client.login_with_browser_cookies()          # インストール済みブラウザを順に探す
client.login_with_browser_cookies("firefox") # ブラウザを指定する
```

追加依存が必要です。

```bash
pip install "niconico.py[browser]"
```

ブラウザで https://www.nicovideo.jp/ にログインした状態にしておいてください。認証情報がライブラリを通ることはなく、保存済みの `user_session` クッキーを読み取るだけです。

!!! warning "login_with_mail は使用できません"
    ニコニコのログインが SPA 化され、フォームが Cloudflare Turnstile で保護されたため、メールアドレスとパスワードだけで完結するログインは行えなくなりました。`login_with_mail` は `LoginFailureError` を送出します。`login_with_browser_cookies` または `login_with_session` を使用してください。
```

!!! warning
    `user_session` は認証情報です。リポジトリ、Issue、ログ、CI 出力に含めないでください。

## CLI

```bash
niconico -h
```
