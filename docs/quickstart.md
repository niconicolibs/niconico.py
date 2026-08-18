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

セッション文字列が手元に無い場合は、ブラウザでログインしてセッションを取得できます。ログインページが開くので、フォームを送信して認証を完了させてください。

```python
from niconico import NicoNico

client = NicoNico()
client.login_with_browser()
```

!!! note "bot 対策について"
    ログインフォームは Cloudflare Turnstile で保護されています。Playwright が同梱する Chromium ではチャレンジが通らずログインボタンが押せないことが確認されています。`channel="chrome"` で実際にインストールされているブラウザを起動し、`user_data_dir` でプロファイルを再利用することを推奨します。

    ```python
    client.login_with_browser(user_data_dir="./.niconico-profile", channel="chrome")
    ```

`login_with_browser` は追加依存が必要です。

```bash
pip install "niconico.py[browser]"
playwright install chromium
```

!!! warning "login_with_mail は使用できません"
    ニコニコのログインが SPA 化され、フォームが bot 対策で保護されたため、メールアドレスとパスワードだけで完結するログインは行えなくなりました。`login_with_mail` は `LoginFailureError` を送出します。`login_with_browser` または `login_with_session` を使用してください。
```

!!! warning
    `user_session` は認証情報です。リポジトリ、Issue、ログ、CI 出力に含めないでください。

## CLI

```bash
niconico -h
```
