"""This module contains the class that represents a user object."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from niconico.objects.common import EssentialChannel, UserIcon
from niconico.objects.video import EssentialVideo, MylistItem, MylistSortKey, MylistSortOrder, Owner


class SessionRelationships(BaseModel):
    """A class that represents the relationships of a user in a session."""

    is_following: bool = Field(..., alias="isFollowing")


class UserRelationships(BaseModel):
    """A class that represents the relationships of a user."""

    session_user: SessionRelationships = Field(..., alias="sessionUser")
    is_me: bool = Field(default=False, alias="isMe")


class UserLevel(BaseModel):
    """A class that represents the level of a user."""

    current_level: int = Field(..., alias="currentLevel")
    next_level_threshold_experience: int = Field(..., alias="nextLevelThresholdExperience")
    next_level_experience: int = Field(..., alias="nextLevelExperience")
    current_level_experience: int = Field(..., alias="currentLevelExperience")


class UserSNS(BaseModel):
    """A class that represents the SNS of a user."""

    type_: Literal["twitter", "instagram", "youtube", "facebook"] = Field(..., alias="type")
    label: str
    icon_url: str = Field(..., alias="iconUrl")
    screen_name: str = Field(..., alias="screenName")
    url: str


class UserCoverImage(BaseModel):
    """A class that represents the cover image of a user."""

    ogp_url: str = Field(..., alias="ogpUrl")
    pc_url: str = Field(..., alias="pcUrl")
    smartphone_url: str = Field(..., alias="smartphoneUrl")


class NicoUser(BaseModel):
    """A class that represents a user object."""

    description: str
    decorated_description_html: str = Field(..., alias="decoratedDescriptionHtml")
    stripped_description: str = Field(..., alias="strippedDescription")
    is_premium: bool = Field(..., alias="isPremium")
    registered_version: str = Field(..., alias="registeredVersion")
    followee_count: int = Field(..., alias="followeeCount")
    follower_count: int = Field(..., alias="followerCount")
    user_level: UserLevel = Field(..., alias="userLevel")
    user_channel: EssentialChannel | None = Field(..., alias="userChannel")
    is_nicorepo_readable: bool = Field(..., alias="isNicorepoReadable")
    sns: list[UserSNS] = Field(..., alias="sns")
    cover_image: UserCoverImage | None = Field(..., alias="coverImage")
    id_: int = Field(..., alias="id")
    nickname: str
    icons: UserIcon


class OwnNicoUser(NicoUser):
    """A class that represents the user object of the own user."""

    niconico_point: int = Field(..., alias="niconicoPoint")
    language: str
    premium_ticket_expire_time: str | None = Field(..., alias="premiumTicketExpireTime")
    creator_patronizing_score: int = Field(..., alias="creatorPatronizingScore")
    is_mail_bounced: bool = Field(..., alias="isMailBounced")
    is_nicorepo_auto_posted_to_twitter: bool = Field(..., alias="isNicorepoAutoPostedToTwitter")


class RelationshipUser(BaseModel):
    """A class that represents a relationship user object."""

    type_: Literal["relationship"] = Field(..., alias="type")
    relationships: UserRelationships
    is_premium: bool = Field(..., alias="isPremium")
    description: str
    stripped_description: str = Field(..., alias="strippedDescription")
    short_description: str = Field(..., alias="shortDescription")
    id_: int = Field(..., alias="id")
    nickname: str
    icons: UserIcon


class RelationshipUsersSummary(BaseModel):
    """A class that represents the summary of a relationship users response from the NvAPI."""

    followees: int
    followers: int
    has_next: bool = Field(..., alias="hasNext")
    cursor: str


class VideoItemSeries(BaseModel):
    """A class that represents a series of a video item."""

    id_: int = Field(..., alias="id")
    title: str
    order: int


class UserVideoItem(BaseModel):
    """A class that represents a video item of a user."""

    series: VideoItemSeries | None
    essential: EssentialVideo


UserVideosSortKey = Literal[
    "registeredAt",
    "viewCount",
    "lastCommentTime",
    "commentCount",
    "likeCount",
    "mylistCount",
    "duration",
]

UserVideosSortOrder = Literal["asc", "desc"]


class OwnVideosLimitationUser(BaseModel):
    """A class that represents the user of the limitation of own videos."""

    uploadable_count: int | None = Field(None, alias="uploadableCount")
    uploaded_count_for_limitation: int | None = Field(None, alias="uploadedCountForLimitation")


class OwnVideosLimitation(BaseModel):
    """A class that represents the limitation of own videos."""

    border_id: int = Field(..., alias="borderId")
    user: OwnVideosLimitationUser


class OwnVideoItem(BaseModel):
    """A class that represents a video item of own videos."""

    is_capture_tweet_allowed: bool = Field(..., alias="isCaptureTweetAllowed")
    is_clip_tweet_allowed: bool = Field(..., alias="isClipTweetAllowed")
    is_community_member_only: bool = Field(..., alias="isCommunityMemberOnly")
    description: str
    is_hidden: bool = Field(..., alias="isHidden")
    is_deleted: bool = Field(..., alias="isDeleted")
    is_cpp_registered: bool = Field(..., alias="isCppRegistered")
    is_contents_tree_exists: bool = Field(..., alias="isContentsTreeExists")
    publish_timer_detail: str | None = Field(..., alias="publishTimerDetail")
    auto_delete_detail: str | None = Field(..., alias="autoDeleteDetail")
    is_exclude_from_upload_list: bool = Field(..., alias="isExcludeFromUploadList")
    like_count: int = Field(..., alias="likeCount")
    gift_point: int = Field(..., alias="giftPoint")
    essential: EssentialVideo
    series: VideoItemSeries | None


class UserMylistItem(BaseModel):
    """A class that represents a mylist item of a user."""

    id_: int = Field(..., alias="id")
    is_public: bool = Field(..., alias="isPublic")
    name: str
    description: str
    decorated_description_html: str = Field(..., alias="decoratedDescriptionHtml")
    default_sort_key: MylistSortKey = Field(..., alias="defaultSortKey")
    default_sort_order: MylistSortOrder = Field(..., alias="defaultSortOrder")
    items_count: int = Field(..., alias="itemsCount")
    owner: Owner
    sample_items: list[MylistItem] = Field(..., alias="sampleItems")
    follower_count: int = Field(..., alias="followerCount")
    created_at: str = Field(..., alias="createdAt")
    is_following: bool = Field(..., alias="isFollowing")


class UserSeriesOwner(BaseModel):
    """A class that represents the owner of a user series item."""

    type_: Literal["user"] = Field(..., alias="type")
    id_: str = Field(..., alias="id")


class UserSeriesItem(BaseModel):
    """A class that represents a series item of a user."""

    id_: int = Field(..., alias="id")
    owner: UserSeriesOwner
    title: str
    is_listed: bool = Field(..., alias="isListed")
    description: str
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    items_count: int = Field(..., alias="itemsCount")


class UserSeriesThumbnails(BaseModel):
    """A class that represents the thumbnails of a user series."""

    default: str
    default_for_owner: str = Field(..., alias="defaultForOwner")
