# ユーザー

## ユーザー情報を取得する

```python
from niconico import NicoNico

client = NicoNico()
user = client.user.get_user("4")

if user is not None:
    print(user.nickname)
```

## 投稿動画を取得する

```python
from niconico import NicoNico

client = NicoNico()
videos = client.user.get_user_videos("4", sort_key="registeredAt", sort_order="desc")

if videos is not None:
    for item in videos.items:
        print(item.essential.title)
```

## 自分の情報を取得する

```python
from niconico import NicoNico

client = NicoNico()
client.login_with_session("user_session_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

own = client.user.get_own()
if own is not None:
    print(own.nickname)
```

ログインが必要な API では `user_session` を設定してください。
