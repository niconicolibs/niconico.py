# niconico.py - Video # TODO: middleが何なのか調べる。

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, Literal, Optional, List, Any

from ..base import DictFromAttribute
from .__init__ import Unknown

if TYPE_CHECKING:
    from ..video import Client as VideoClient, Video as RealVideo


__all__ = (
    "NicoDic", "Phrase", "EasyComment", "TagEdit", "TagItem", "Tag", "Counter", "Thumbnail",
    "Rating", "ViewerLike", "Viewer", "AbcOwner", "AbcVideo", "Video", "VideoOwner",
    "MyListOwner", "MyListItemVideo", "MyListItem", "MyList"
)


# easyComment
class NicoDic(DictFromAttribute):
    "ニコニコ大百科での簡易データです。"

    title: str
    viewTitle: str
    summary: str
    link: str


class Phrase(DictFromAttribute):
    "言葉です。"

    text: str
    "言葉です。"
    nicodic: NicoDic
    "ニコニコ大百科のデータです。"


class EasyComment(DictFromAttribute):
    "簡易コメントリストです。"

    phrases: List[Phrase]
    "簡易コメントリストのデータです。"


# tag
class TagEdit(DictFromAttribute):
    "タグを編集可能かどうかのデータです。"

    isEditable: bool
    "編集可能かどうかです。"
    uneditableReason: Optional[Literal["NEED_LOGIN"]]
    "タグを編集できない理由です。"
    editKey: Optional[str]
    "不明"


class TagItem(DictFromAttribute):
    "タグの内容です。"

    name: str
    "タグの名前"
    isCategory: bool
    "不明"
    isCategoryCandidate: bool
    "不明"
    isNicodicArticleExists: bool
    "不明"
    isLocked: bool
    "ロックされているかどうかです。"


class Tag(DictFromAttribute):
    "タグデータです。"

    items: List[TagItem]
    "ついているタグのリストです。"
    hasR18Tag: bool
    "センシティブなタグがあるかどうかです。"
    isPublishedNicoscript: bool
    "不明"
    edit: TagEdit
    "編集できるかのデータです。"
    viewer: Optional[TagEdit]
    "不明"


# video
class Counter(DictFromAttribute):
    "動画の閲覧数等のカウンターです。"

    view: int
    "閲覧数"
    comment: int
    "コメント数"
    mylist: int
    "マイリスト数"
    like: int
    "「好き」数"


class Thumbnail(DictFromAttribute):
    "サムネイルです。"

    url: str
    "サムネイルの画像のURLです。"
    middleUrl: str
    "不明"
    largeUrl: str
    "不明"
    player: str
    "不明"
    ogp: str
    "不明"


class Rating(DictFromAttribute):
    "動画の評価です。"

    isAdult: bool
    "大人向けかどうかです。"


class ViewerLike(DictFromAttribute):
    "クライアントの動画へやった「好き」のデータです。"

    isLiked: bool
    "「好き」を押したかどうかです。"
    count: Any
    "不明"


class Viewer(DictFromAttribute):
    "動画でのクライアントの内容です。"

    isOwner: bool
    "動画投稿者かどうかです。"
    like: ViewerLike
    "動画へやった「好き」のデータです。"


class AbcOwner(DictFromAttribute):
    "動画投稿者の基底クラスです。"

    id: str
    "投稿者のIDです。"
    name: str
    "投稿者の名前です。"
    iconUrl: str
    "投稿者のアイコンのURLです。"


class AbcVideo(DictFromAttribute["VideoClient"]):
    "動画データの基底クラスです。"

    id: str
    "動画IDです。"
    title: str
    "動画のタイトルです。"
    description: str
    "動画の説明です。"
    count: Counter
    "動画の閲覧数等のデータです。"
    duration: int
    "動画の長さです。"
    thumbnail: Thumbnail
    "動画のサムネイルです。"
    registeredAt: str
    "動画のアップロードされた時間です。"


class VideoOwner(AbcOwner):
    "動画の投稿者のデータです。"

    isVideosPublic: bool
    "アップロードした動画が公開されているかどうかです。"
    isMylistsPublic: bool
    "マイリストが公開されているかどうかです。"


class Video(AbcVideo):
    "動画データです。"

    rating: Rating
    "動画のレートです。"
    isPrivate: bool
    "プライベートかどうかです。"
    isDeleted: bool
    "削除済みかどうかです。"
    isNoBanner: bool
    "不明"
    isAuthenticationRequired: bool
    "不明"
    isEmbedPlayerAllowed: bool
    "埋め込み動画プレイヤーが有効かどうかです。"
    isGiftAllowed: bool
    "ギフトが有効かどうかです。"
    viewer: Viewer
    "クライアントのデータです。"
    watchableUserTypeForPayment: str # TODO: ここに入る文字列は決まっている、なのでLiteralにしたい。
    "不明"
    commentableUserTypeForPayment: str # TODO: 上記と同じ。
    "不明"


class MyListOwner(AbcOwner):
    "マイリストのオーナーのデータです。"

    ownerType: str
    "不明"


class MyListItemVideo(AbcVideo):
    "マイリストのアイテムの動画です。"

    type: str # TODO: ここに入る文字列は恐らく決まっている...? Literalにしたい。
    "不明"
    shortDescription: str
    "短くした動画の説明です。"
    latestCommentSummary: str
    "最新のコメントの内容です。"
    isChannelVideo: bool
    "不明"
    isPaymentRequired: bool
    "不明"
    playbackPosition: Any # 何なのか調べる。
    "不明"
    owner: MyListOwner
    "マイリストの作成者のデータです。"
    requireSensitiveMasking: bool
    "センシティブなもので一度隠す必要があるかどうかです。"
    videoLive: Any # TODO: なんなのか調べる。
    "不明"

    def get_video(self) -> RealVideo:
        ":class:`niconico.video.Video` のインスタンスを作ります。"
        return self.__super__.get_video(self.url)

    @property
    def url(self) -> str:
        "この動画のURLです。"
        return f"https://www.nicovideo.jp/watch/{self.id}"


class MyListItem(DictFromAttribute["VideoClient"]):
    "マイリストのアイテムです。"

    __extends__ = {
        "video": MyListItemVideo
    }

    itemId: int
    "アイテムIDです。"
    watchId: str
    "アイテムの動画IDです。"
    description: str
    "アイテムの説明です。"
    addedAt: str
    "マイリストに追加された時間です。"
    status: str # TODO: ここに入っているのは決まっていると思うのでLiteralにしたい。
    "公開されているなら`public`が入ります。"
    video: MyListItemVideo
    "動画情報のクラスです。"


class MyList(DictFromAttribute["VideoClient"]):
    "一ページ単位でのマイリストです。"

    __extends__ = {
        "items": MyListItem
    }

    id: str
    "マイリストのIDです。"
    name: str
    "マイリストの名前です。"
    description: str
    "マイリストの説明です。"
    defaultSortKey: str
    "不明"
    defaultSortOrder: str
    "不明"
    items: list[MyListItem]
    "マイリストに入っている動画のアイテムのリストです。"
    totalItemCount: int
    "マイリストにあるアイテムの数です。"
    hasNext: bool
    "分割されたマイリストのアイテムリストのページで次のページがあるかどうかです。"
    isPublic: bool
    "公開されているかどうかです。"
    owner: MyListOwner
    "マイリストの作成者の情報です。"
    hasInvisibleItems: bool
    "不明"
    followerCount: int
    "フォロワーの数です。"
    isFollowing: bool
    "フォローしているかどうかです。"