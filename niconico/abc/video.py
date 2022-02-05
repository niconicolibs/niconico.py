# niconico.py - Video

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict, Literal, Optional, List

from ..base import DictFromAttribute
from .__init__ import Unknown

if TYPE_CHECKING:
    from ..video import Client as VideoClient, Video as RealVideo


# easyComment
class NicoDic(DictFromAttribute):
    title: str
    viewTitle: str
    summary: str
    link: str


class Phrase(DictFromAttribute):
    text: str
    nicodic: NicoDic


class EasyComment(DictFromAttribute):
    phrases: List[Phrase]


# tag
class TagEdit(DictFromAttribute):
    isEditable: bool
    uneditableReason: Optional[Literal["NEED_LOGIN"]]
    editKey: Optional[str]


class TagItem(DictFromAttribute):
    name: str
    isCategory: bool
    isCategoryCandidate: bool
    isNicodicArticleExists: bool
    isLocked: bool


class Tag(DictFromAttribute):
    items: List[TagItem]
    hasR18Tag: bool
    isPublishedNicoscript: bool
    edit: TagEdit
    viewer: Optional[TagEdit]


# video
class Counter(DictFromAttribute):
    view: int
    comment: int
    mylist: int
    like: int


class Thumbnail(DictFromAttribute):
    "サムネイルです。"
    url: str
    middleUrl: str
    largeUrl: str
    player: str
    ogp: str


class Rating(DictFromAttribute):
    isAdult: bool


class ViewerLike(DictFromAttribute):
    isLiked: bool
    count: Unknown


class Viewer(DictFromAttribute):
    isOwner: bool
    like: ViewerLike


class AbcVideo(DictFromAttribute["VideoClient"]):
    "動画データの基底クラスです。"
    id: str
    title: str
    description: str
    count: Counter
    duration: int
    thumbnail: Thumbnail
    registeredAt: str


class Video(AbcVideo):
    "動画データです。"

    rating: Rating
    isPrivate: bool
    isDeleted: bool
    isNoBanner: bool
    isAuthenticationRequired: bool
    isEmbedPlayerAllowed: bool
    isGiftAllowed: bool
    viewer: Viewer
    watchableUserTypeForPayment: str # TODO: ここに入る文字列は決まっている、なのでLiteralにしたい。
    commentableUserTypeForPayment: str # TODO: 上記と同じ。


class MyListOwner(DictFromAttribute):
    "マイリストのオーナーのデータです。"

    ownerType: str
    id: str
    name: str
    iconUrl: str


class MyListItemVideo(AbcVideo):
    "マイリストのアイテムの動画です。"

    type: str # TODO: ここに入る文字列は恐らく決まっている...? Literalにしたい。
    duration: int
    shortDescription: str
    latestCommentSummary: str
    isChannelVideo: bool
    isPaymentRequired: bool
    playbackPosition: None
    owner: MyListOwner
    requireSensitiveMasking: bool
    videoLive: None

    def get_video(self) -> RealVideo:
        ":class:`niconico.video.Video` のインスタンスを作ります。"
        return self.super_.get_video(self.url)

    @property
    def url(self) -> str:
        "この動画のURLです。"
        return f"https://www.nicovideo.jp/watch/{self.id}"


class MyListItem(DictFromAttribute["VideoClient"]):
    "マイリストのアイテムです。"

    itemId: int
    watchId: str
    description: str
    addedAt: str
    status: str
    video: MyListItemVideo


class MyList(DictFromAttribute["VideoClient"]):
    """マイリストです。

    Notes
    -----
    マイリストの全ての動画が入っているわけではありません。  
    ページ単位となっています。"""

    id: str
    name: str
    description: str
    defaultSortKey: str
    defaultSortOrder: str
    items: list[MyListItem]
    totalItemCount: int
    hasNext: bool
    isPublic: bool
    owner: MyListOwner
    hasInvisibleItems: bool
    followerCount: int
    isFollowing: bool