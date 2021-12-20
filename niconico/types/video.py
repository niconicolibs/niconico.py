# niconico.py - Video

from typing import Literal, Optional, List

from ..base import DictFromAttribute
from .__init__ import Unknown


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


class Video(DictFromAttribute):
    id: str
    title: str
    description: str
    count: Counter
    duration: int
    thumbnail: Thumbnail
    rating: Rating
    registeredAt: str
    isPrivate: bool
    isDeleted: bool
    isNoBanner: bool
    isAuthenticationRequired: bool
    isEmbedPlayerAllowed: bool
    isGiftAllowed: bool
    viewer: Viewer
    watchableUserTypeForPayment: str # todo: ここに入る文字列は決まっている、なのでLiteralにしたい。
    commentableUserTypeForPayment: str # todo: 上記と同じ。