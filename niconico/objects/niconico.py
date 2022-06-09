# niconico.py - Common

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, Literal, Optional, List, Any

from ..base import DictFromAttribute
from .__init__ import Unknown


__all__ = (
    "Icons", "AbcUser", "UserLevel", "UserChannel", "UserSNS", "User"
    "LoginFailureException"
)


class Icons(DictFromAttribute):
    "ニコニコのアカウントのアイコンURLのクラスです。"

    small: str
    "小さいアイコン画像のURLです。"
    large: str
    "大きいアイコン画像のURLです。"


class AbcUser(DictFromAttribute):
    "ニコニコのアカウントデータの基底クラスです。"

    id: int
    "アカウントのIDです。"
    nickname: str
    "アカウントのニックネームです。"
    description: str
    "アカウントの概要です。"
    strippedDescription: str
    "要約されたアカウントの概要です。"
    isPremium: bool
    "プレミアムかどうかです。"
    icons: Icons
    "アイコンのURL情報です。"


class UserLevel(DictFromAttribute):
    "ニコニコのアカウントのユーザーレベルのクラスです。"

    currentLevel: int
    "アカウントの今のレベルです。"
    nextLevelThresholdExperience: int
    "今のレベルの合計経験値です。"
    nextLevelExperience: int
    "次のレベルまでの経験値です。"
    currentLevelExperience: int
    "今のレベルの経験値です。"


class UserChannel(DictFromAttribute):
    "ニコニコのアカウントの紐付けされたチャンネルのクラスです。"

    id: str
    "チャンネルのIDです。chから始まる文字列です。"
    name: str
    "チャンネルの名前です。"
    description: str
    "チャンネルの概要です。"
    thumbnailUrl: str
    "チャンネルのサムネイルURLです。"
    thumbnailSmallUrl: str
    "チャンネルの小さいサムネイルURLです。"


class UserSNS(DictFromAttribute):
    "ニコニコのアカウントの紐付けされたSNSのクラスです。"

    type: str
    "SNSの種類です。"
    label: str
    "SNSの名称です。"
    iconUrl: str
    "SNSのアイコンのURLです。"
    screenName: str
    "SNSの表示名です。"
    url: str
    "SNSのURLです。"


class User(AbcUser):
    "ニコニコのアカウントデータです。"

    registeredVersion: str
    "アカウントが登録されたときのバージョンです。"
    followeeCount: int
    "フォローされている数です。"
    followerCount: int
    "フォロワーの数です。"
    isNicorepoReadable: bool
    "ニコレポが読み取れるかどうかです。"
    userLevel: UserLevel
    "ユーザーレベルに関する情報です。"
    userChannel: UserChannel
    "ユーザーに紐付けされているチャンネルの情報です。"
    sns: List[UserSNS]
    "アカウントに紐付けられているSNSの一覧です。"


class LoginFailureException(Exception):
    """ログインの失敗を知らせる例外クラスです。"""
    pass