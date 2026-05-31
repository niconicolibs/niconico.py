"""Data models for the watch API response."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

from niconico.objects.video import EssentialVideo


class WatchAPIMeta(BaseModel):
    """Meta data of the watch API response."""

    status: int
    code: str


class MetaTag(BaseModel):
    """Data model of a meta tag."""

    name: str | None = Field(None)
    property_: str | None = Field(None, alias="property")
    content: str


class LinkTag(BaseModel):
    """Data model of a link tag."""

    href: str
    rel: str
    attrs: dict[str, str] | list


class WatchPageMetadata(BaseModel):
    """Data model of the metadata of a watch page."""

    title: str
    meta_tags: list[MetaTag] = Field(..., alias="metaTags")
    link_tags: list[LinkTag] = Field(..., alias="linkTags")
    json_lds: Any = Field(..., alias="jsonLds")


class WatchChannelThumbnail(BaseModel):
    """Data model of the thumbnail of a watch channel."""

    url: str
    small_url: str | None = Field(..., alias="smallUrl")


class WatchChannelViewerFollow(BaseModel):
    """Data model of the viewer follow status of a watch channel."""

    is_followed: bool = Field(..., alias="isFollowed")
    is_bookmarked: bool = Field(..., alias="isBookmarked")
    token: str
    token_timestamp: int = Field(..., alias="tokenTimestamp")


class WatchChannelViewer(BaseModel):
    """Data model of the viewer of a watch channel."""

    follow: WatchChannelViewerFollow


class WatchChannel(BaseModel):
    """Data model of a watch channel."""

    id_: str = Field(..., alias="id")
    name: str
    is_official_anime: bool = Field(..., alias="isOfficialAnime")
    is_display_ad_banner: bool = Field(..., alias="isDisplayAdBanner")
    thumbnail: WatchChannelThumbnail
    viewer: WatchChannelViewer


class WatchOwnerChannel(BaseModel):
    """Data model of a watch owner channel."""

    id_: str = Field(..., alias="id")
    name: str
    url: str


class WatchClient(BaseModel):
    """Data model of the client of the watch API response."""

    nicosid: str | None
    watch_id: str = Field(..., alias="watchId")
    watch_track_id: str = Field(..., alias="watchTrackId")


class CommentThreadId(BaseModel):
    """Data model of a comment thread ID."""

    id_: int = Field(..., alias="id")
    fork: int
    fork_label: str = Field(..., alias="forkLabel")


class CommentLayer(BaseModel):
    """Data model of a comment layer."""

    index: int
    is_translucent: bool = Field(..., alias="isTranslucent")
    thread_ids: list[CommentThreadId] = Field(..., alias="threadIds")


class CommentThread(BaseModel):
    """Data model of a comment thread."""

    id_: int = Field(..., alias="id")
    fork: int
    fork_label: str = Field(..., alias="forkLabel")
    video_id: str = Field(..., alias="videoId")
    is_active: bool = Field(..., alias="isActive")
    is_default_post_target: bool = Field(..., alias="isDefaultPostTarget")
    is_easy_comment_post_target: bool = Field(..., alias="isEasyCommentPostTarget")
    is_leaf_required: bool = Field(..., alias="isLeafRequired")
    is_owner_thread: bool = Field(..., alias="isOwnerThread")
    is_threadkey_required: bool = Field(..., alias="isThreadkeyRequired")
    threadkey: str | None = Field(..., alias="threadkey")
    is_184_forced: bool = Field(..., alias="is184Forced")
    has_nicoscript: bool = Field(..., alias="hasNicoscript")
    label: str
    postkey_status: int = Field(..., alias="postkeyStatus")
    server: str


class CommentNgScore(BaseModel):
    """Data model of the score of a comment NG."""

    is_disabled: bool = Field(..., alias="isDisabled")


class CommentNgViewerItem(BaseModel):
    """Data model of an item of a comment NG viewer."""

    type_: str = Field(..., alias="type")
    source: str
    registered_at: str = Field(..., alias="registeredAt")


class CommentNgViewer(BaseModel):
    """Data model of a comment NG viewer."""

    revision: int
    count: int
    items: list[CommentNgViewerItem]


class CommentNg(BaseModel):
    """Data model of a comment NG."""

    ng_score: CommentNgScore = Field(..., alias="ngScore")
    channel: list
    owner: list
    viewer: CommentNgViewer | None


class NvCommentDataTarget(BaseModel):
    """Data model of a target of an NV comment data."""

    id_: str = Field(..., alias="id")
    fork: str


class NvCommentDataParams(BaseModel):
    """Data model of the parameters of an NV comment data."""

    targets: list[NvCommentDataTarget]
    language: str


class NvCommentData(BaseModel):
    """Data model of an NV comment data."""

    thread_key: str = Field(..., alias="threadKey")
    server: str
    params: NvCommentDataParams


class WatchComment(BaseModel):
    """Data model of the comment of the watch API response."""

    layers: list[CommentLayer]
    threads: list[CommentThread]
    ng: CommentNg
    is_attention_required: bool = Field(..., alias="isAttentionRequired")
    nv_comment: NvCommentData = Field(..., alias="nvComment")


class EasyCommentNicodic(BaseModel):
    """Data model of a Nicodic of an easy comment."""

    title: str
    view_title: str = Field(..., alias="viewTitle")
    summary: str
    link: str


class EasyCommentPhrase(BaseModel):
    """Data model of a phrase of an easy comment."""

    text: str
    nicodic: EasyCommentNicodic | None


class WatchEasyComment(BaseModel):
    """Data model of an easy comment of the watch API response."""

    phrases: list[EasyCommentPhrase]


class WatchGenre(BaseModel):
    """Data model of a genre of the watch API response."""

    key: str
    label: str
    is_immoral: bool = Field(..., alias="isImmoral")
    is_disabled: bool = Field(..., alias="isDisabled")
    is_not_set: bool = Field(..., alias="isNotSet")


class WatchMediaDomandVideo(BaseModel):
    """Data model of a video of a watch media DOMAND."""

    id_: str = Field(..., alias="id")
    is_available: bool = Field(..., alias="isAvailable")
    label: str
    bit_rate: int = Field(..., alias="bitRate")
    width: int
    height: int
    quality_level: int = Field(..., alias="qualityLevel")
    recommended_highest_audio_quality_level: int = Field(..., alias="recommendedHighestAudioQualityLevel")


class AudioLoudness(BaseModel):
    """Data model of the loudness of an audio."""

    type_: str = Field(..., alias="type")
    value: float


class WatchMediaDomandAudio(BaseModel):
    """Data model of an audio of a watch media DOMAND."""

    id_: str = Field(..., alias="id")
    is_available: bool = Field(..., alias="isAvailable")
    bit_rate: int = Field(..., alias="bitRate")
    sampling_rate: int = Field(..., alias="samplingRate")
    integrated_loudness: float = Field(..., alias="integratedLoudness")
    true_peak: float = Field(..., alias="truePeak")
    quality_level: int = Field(..., alias="qualityLevel")
    loudness_collection: list[AudioLoudness] = Field(..., alias="loudnessCollection")


class WatchMediaDomand(BaseModel):
    """Data model of a watch media DOMAND."""

    videos: list[WatchMediaDomandVideo]
    audios: list[WatchMediaDomandAudio]
    is_storyboard_available: bool = Field(..., alias="isStoryboardAvailable")
    access_right_key: str = Field(..., alias="accessRightKey")


class WatchMedia(BaseModel):
    """Data model of the media of the watch API response."""

    domand: WatchMediaDomand
    delivery: None
    delivery_legacy: None = Field(..., alias="deliveryLegacy")


class WatchOwnerViewer(BaseModel):
    """Data model of a viewer of a watch owner."""

    is_following: bool = Field(..., alias="isFollowing")


class WatchOwnerLive(BaseModel):
    """Data model of a live stream of a watch owner."""

    id_: str = Field(..., alias="id")
    title: str
    url: str
    begun_at: str = Field(..., alias="begunAt")
    is_video_live: bool = Field(..., alias="isVideoLive")
    video_live_on_air_start_time: str | None = Field(..., alias="videoLiveOnAirStartTime")
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    flip_thumbnail_url: str | None = Field(..., alias="flipThumbnailUrl")


class WatchOwner(BaseModel):
    """Data model of a watch owner."""

    id_: int = Field(..., alias="id")
    nickname: str
    icon_url: str = Field(..., alias="iconUrl")
    channel: WatchOwnerChannel | None
    live: WatchOwnerLive | None
    is_videos_public: bool = Field(..., alias="isVideosPublic")
    is_mylists_public: bool = Field(..., alias="isMylistsPublic")
    video_live_notice: None = Field(..., alias="videoLiveNotice")
    viewer: WatchOwnerViewer | None


class WatchPaymentVideo(BaseModel):
    """Data model of a video of a watch payment."""

    is_ppv: bool = Field(..., alias="isPpv")
    is_admission: bool = Field(..., alias="isAdmission")
    is_continuation_benefit: bool = Field(..., alias="isContinuationBenefit")
    is_premium: bool = Field(..., alias="isPremium")
    watchable_user_type: str = Field(..., alias="watchableUserType")
    commentable_user_type: str = Field(..., alias="commentableUserType")
    billing_type: str = Field(..., alias="billingType")


class WatchPaymentPreviewCheck(BaseModel):
    """Data model of a check of a watch payment preview."""

    is_enabled: bool = Field(..., alias="isEnabled")


class WatchPaymentPreview(BaseModel):
    """Data model of a preview of a watch payment."""

    ppv: WatchPaymentPreviewCheck
    admission: WatchPaymentPreviewCheck
    continuation_benefit: WatchPaymentPreviewCheck = Field(..., alias="continuationBenefit")
    premium: WatchPaymentPreviewCheck


class WatchPayment(BaseModel):
    """Data model of a payment of the watch API response."""

    video: WatchPaymentVideo
    preview: WatchPaymentPreview


class PlayerInitialPlayback(BaseModel):
    """Data model of the initial playback of a player."""

    type_: str = Field(..., alias="type")
    position_sec: float | None = Field(None, alias="positionSec")


class WatchPlayerComment(BaseModel):
    """Data model of a comment of a watch player."""

    is_default_invisible: bool = Field(..., alias="isDefaultInvisible")


class WatchPlayer(BaseModel):
    """Data model of a player of the watch API response."""

    initial_playback: PlayerInitialPlayback | None = Field(..., alias="initialPlayback")
    comment: WatchPlayerComment
    layer_mode: int = Field(..., alias="layerMode")


class RankingGenre(BaseModel):
    """Data model of a genre of a ranking."""

    rank: int
    genre: str
    date_time: str = Field(..., alias="dateTime")


class RankingTag(BaseModel):
    """Data model of a tag of a ranking."""

    tag: str
    regularized_tag: str = Field(..., alias="regularizedTag")
    rank: int
    genre: str
    date_time: str = Field(..., alias="dateTime")


class WatchRanking(BaseModel):
    """Data model of a ranking of the watch API response."""

    genre: RankingGenre | None
    popular_tag: list[RankingTag] = Field(..., alias="popularTag")


class WatchSeriesVideos(BaseModel):
    """Data model of the videos of a watch series."""

    prev: EssentialVideo | None
    next_: EssentialVideo | None = Field(..., alias="next")
    first: EssentialVideo | None


class WatchSeries(BaseModel):
    """Data model of a series of the watch API response."""

    id_: int = Field(..., alias="id")
    title: str
    description: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    video: WatchSeriesVideos


class WatchSystem(BaseModel):
    """Data model of the system of the watch API response."""

    server_time: str = Field(..., alias="serverTime")
    is_peak_time: bool = Field(..., alias="isPeakTime")
    is_stella_alive: bool = Field(..., alias="isStellaAlive")


class WatchTagItem(BaseModel):
    """Data model of a tag item."""

    name: str
    is_category: bool = Field(..., alias="isCategory")
    is_category_candidate: bool = Field(..., alias="isCategoryCandidate")
    is_nicodic_article_exists: bool = Field(..., alias="isNicodicArticleExists")
    is_locked: bool = Field(..., alias="isLocked")


class WatchTagEdit(BaseModel):
    """Data model of an edit of a watch tag."""

    is_editable: bool = Field(..., alias="isEditable")
    uneditable_reason: str | None = Field(..., alias="uneditableReason")
    edit_key: str | None = Field(..., alias="editKey")


class WatchTag(BaseModel):
    """Data model of a tag of the watch API response."""

    items: list[WatchTagItem]
    has_r18_tag: bool = Field(..., alias="hasR18Tag")
    is_published_nicoscript: bool = Field(..., alias="isPublishedNicoscript")
    edit: WatchTagEdit
    viewer: WatchTagEdit | None


class WatchVideoCount(BaseModel):
    """Data model of the count of a watch video."""

    view: int
    comment: int
    mylist: int
    like: int


class WatchVideoThumbnail(BaseModel):
    """Data model of a thumbnail of a watch video."""

    url: str
    middle_url: str | None = Field(..., alias="middleUrl")
    large_url: str | None = Field(..., alias="largeUrl")
    player: str
    ogp: str


class WatchVideoRating(BaseModel):
    """Data model of the rating of a watch video."""

    is_adult: bool = Field(..., alias="isAdult")


class WatchVideoViewerLike(BaseModel):
    """Data model of the like status of a viewer of a watch video."""

    is_liked: bool = Field(..., alias="isLiked")
    count: int | None


class WatchVideoViewer(BaseModel):
    """Data model of a viewer of a watch video."""

    is_owner: bool = Field(..., alias="isOwner")
    like: WatchVideoViewerLike


class WatchVideo(BaseModel):
    """Data model of a video of the watch API response."""

    id_: str = Field(..., alias="id")
    title: str
    description: str
    count: WatchVideoCount
    duration: int
    thumbnail: WatchVideoThumbnail
    rating: WatchVideoRating
    registered_at: str = Field(..., alias="registeredAt")
    is_private: bool = Field(..., alias="isPrivate")
    is_deleted: bool = Field(..., alias="isDeleted")
    is_no_banner: bool = Field(..., alias="isNoBanner")
    is_authentication_required: bool = Field(..., alias="isAuthenticationRequired")
    is_embed_player_allowed: bool = Field(..., alias="isEmbedPlayerAllowed")
    is_gift_allowed: bool = Field(..., alias="isGiftAllowed")
    viewer: WatchVideoViewer | None
    watchable_user_type_for_payment: str = Field(..., alias="watchableUserTypeForPayment")
    commentable_user_type_for_payment: str = Field(..., alias="commentableUserTypeForPayment")


class WatchViewerExistence(BaseModel):
    """Data model of the existence of a watch viewer."""

    age: int
    prefecture: str
    sex: str


class WatchViewer(BaseModel):
    """Data model of a viewer of the watch API response."""

    id_: int = Field(..., alias="id")
    nickname: str
    is_premium: bool = Field(..., alias="isPremium")
    allow_sensitive_contents: bool = Field(..., alias="allowSensitiveContents")
    existence: WatchViewerExistence


class WatchVideoLive(BaseModel):
    """Data model of a live video of the watch API response."""

    program_id: str = Field(..., alias="programId")
    begin_at: str = Field(..., alias="beginAt")
    end_at: str = Field(..., alias="endAt")


class WatchData(BaseModel):
    """Data model of the data of the watch API response."""

    ads: None
    category: None
    channel: WatchChannel | None
    client: WatchClient
    comment: WatchComment
    community: None
    easy_comment: WatchEasyComment = Field(..., alias="easyComment")
    external: Any
    genre: WatchGenre
    marquee: Any
    media: WatchMedia
    ok_reason: str = Field(..., alias="okReason")
    owner: WatchOwner | None
    payment: WatchPayment
    pc_watch_page: Any = Field(..., alias="pcWatchPage")
    player: WatchPlayer
    ppv: None
    ranking: WatchRanking
    series: WatchSeries | None
    smartphone: None
    system: WatchSystem
    tag: WatchTag
    video: WatchVideo
    video_ads: Any = Field(..., alias="videoAds")
    video_live: WatchVideoLive | None = Field(..., alias="videoLive")
    viewer: WatchViewer | None
    waku: Any


class WatchResponseError(BaseModel):
    """Data model of the error response of the watch API."""

    is_custom_error: bool = Field(..., alias="isCustomError")
    status_code: int = Field(..., alias="statusCode")
    error_code: str = Field(..., alias="errorCode")
    reason_code: str | None = Field(..., alias="reasonCode")
    deleted_message: str | None = Field(..., alias="deletedMessage")
    community_link: str | None = Field(..., alias="communityLink")
    publish_scheduled_at: str | None = Field(..., alias="publishScheduledAt")
    data: None


class WatchAPIData(BaseModel):
    """Data model of the data of the watch API response."""

    metadata: WatchPageMetadata
    google_tag_manager: Any | None = Field(..., alias="googleTagManager")
    response: WatchData


class WatchAPIErrorData(BaseModel):
    """Data model of an error response of the watch API."""

    metadata: WatchPageMetadata
    response: WatchResponseError


T = TypeVar("T")


class WatchAPIResponse(BaseModel, Generic[T]):
    """Data model of the watch API response.

    ref: https://www.nicovideo.jp/watch/<video_id>?responseType=json
    """

    meta: WatchAPIMeta
    data: T


class StoryboardImage(BaseModel):
    """Data model of an image of a storyboard."""

    timestamp: int
    url: str


class StoryboardResponse(BaseModel):
    """Data model of the storyboard response.

    ref: https://asset.domand.nicovideo.jp/<id>/storyboard/~~~
    """

    columns: int
    images: list[StoryboardImage]
    interval: int
    rows: int
    thumbnail_height: int = Field(..., alias="thumbnailHeight")
    thumbnail_width: int = Field(..., alias="thumbnailWidth")
    version: str


class NvCommentAPIMeta(BaseModel):
    """Data model of the NV comment API meta."""

    status: int
    error_code: str | None = Field(None, alias="errorCode")


class GlobalComment(BaseModel):
    """Data model of a global comment."""

    id_: str = Field(..., alias="id")
    count: int


class Comment(BaseModel):
    """Data model of a comment."""

    body: str
    commands: list[str]
    id_: str = Field(..., alias="id")
    is_my_post: bool = Field(..., alias="isMyPost")
    is_premium: bool = Field(..., alias="isPremium")
    nicoru_count: int = Field(..., alias="nicoruCount")
    nicoru_id: str | None = Field(None, alias="nicoruId")
    no: int
    posted_at: str = Field(..., alias="postedAt")
    score: int
    source: str
    user_id: str = Field(..., alias="userId")
    vpos_ms: int = Field(..., alias="vposMs")


class NvCommentThread(BaseModel):
    """Data model of an NV comment thread."""

    id_: str = Field(..., alias="id")
    fork: str
    comment_count: int = Field(..., alias="commentCount")
    comments: list[Comment]


class NvCommentAPIData(BaseModel):
    """Data model of the NV comment data."""

    global_comments: list[GlobalComment] = Field(..., alias="globalComments")
    threads: list[NvCommentThread]


class NvCommentAPIResponse(BaseModel):
    """Data model of the NV comment API response.

    ref: https://public.nvcomment.nicovideo.jp/v1/threads
    """

    data: NvCommentAPIData | None
    meta: NvCommentAPIMeta
