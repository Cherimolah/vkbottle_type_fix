import enum
import json
import typing
from typing import Optional, Union, List
from abc import ABC

from vkbottle.api.api import API, ABCAPI
from vkbottle.dispatch.views.bot import ABCBotMessageView, BotMessageView
from vkbottle.tools.mini_types.bot import MessageMin
from vkbottle.tools.mini_types.base.message import BaseMessageMin
from vkbottle_types.codegen.objects import VideoVideo, VideoVideoFull, PollsPoll
from vkbottle_types.objects import MessagesMessageAttachment, MessagesMessage, MessagesForeignMessage
from vkbottle_types.events.objects.group_event_objects import MessageNewObject
from vkbottle_types.events.bot_events import MessageNew
from vkbottle_types.base_model import BaseModel

from pydantic import Field


class VideoVideoTypeExtended(enum.Enum):
    VIDEO = "video"
    MUSIC_VIDEO = "music_video"
    MOVIE = "movie"
    LIVE = "live"
    SHORT_VIDEO = "short_video"
    VIDEO_MESSAGE = 'video_message'


class MessagesMessageAttachmentTypeExtended(enum.Enum):
    PHOTO = "photo"
    AUDIO = "audio"
    VIDEO = "video"
    VIDEO_PLAYLIST = "video_playlist"
    DOC = "doc"
    LINK = "link"
    MARKET = "market"
    GIFT = "gift"
    STICKER = "sticker"
    WALL = "wall"
    WALL_REPLY = "wall_reply"
    ARTICLE = "article"
    POLL = "poll"
    CALL = "call"
    GRAFFITI = "graffiti"
    AUDIO_MESSAGE = "audio_message"
    NARRATIVE = "narrative"


class NarrativeType(BaseModel):
    can_see: Optional[bool] = Field(default=None)
    seen: Optional[bool] = Field(default=None)
    id: Optional[int] = Field(default=None)
    is_delete: Optional[bool] = Field(default=None)
    is_favorite: Optional[bool] = Field(default=None)
    owner_id: Optional[int] = Field(default=None)
    title: Optional[str] = Field(default=None)
    views: Optional[int] = Field(default=None)


class VideoVideoExtended(VideoVideo):
    type: typing.Optional["VideoVideoTypeExtended"] = Field(default=None)


class VideoVideoFullExtended(VideoVideoExtended, VideoVideoFull):
    pass


class PollsPollExtended(PollsPoll):
    anonymous: bool = Field(default=None)


class MessagesMessageAttachmentExtended(MessagesMessageAttachment):
    video: Optional["VideoVideoFullExtended"] = None
    poll: Optional["PollsPollExtended"] = None
    narrative: Optional["NarrativeType"] = None
    type: Optional["MessagesMessageAttachmentTypeExtended"]


class MessagesForeignMessageExtended(MessagesForeignMessage):
    attachments: Optional[List["MessagesMessageAttachmentExtended"]] = None
    reply_message: Optional["MessagesForeignMessageExtended"] = None
    fwd_messages: Optional[List["MessagesForeignMessageExtended"]] = None


class MessagesMessageExtended(MessagesMessage):
    attachments: Optional[List["MessagesMessageAttachmentExtended"]] = None
    reply_message: Optional["MessagesForeignMessageExtended"] = None
    fwd_messages: Optional[List["MessagesForeignMessageExtended"]] = None


class MessageNewObjectExtended(MessageNewObject):
    message: Optional["MessagesMessageExtended"] = None


class MessageNewExtended(MessageNew):
    object: MessageNewObjectExtended


class BaseMessageMinExtended(MessagesMessageExtended, BaseMessageMin):
    pass


class MessageMinExtended(BaseMessageMinExtended, MessageMin):
    pass


MessagesForeignMessageExtended.update_forward_refs()


def message_min(event: dict, ctx_api: "ABCAPI", replace_mention: bool = True) -> "MessageMin":
    update = MessageNewExtended(**event)

    if update.object.message is None:
        msg = "Please set longpoll to latest version"
        raise RuntimeError(msg)

    return MessageMinExtended(
        **update.object.message.dict(),
        client_info=update.object.client_info,
        group_id=update.group_id,
        replace_mention=replace_mention,
        unprepared_ctx_api=ctx_api,
    )


class ABCBotMessageViewExtended(ABCBotMessageView, ABC):
    @staticmethod
    async def get_message(
            event: dict, ctx_api: Union["API", "ABCAPI"], replace_mention: bool
    ) -> "MessageMin":
        message = message_min(event, ctx_api, replace_mention)
        if isinstance(message.payload, str):
            message.payload = json.loads(message.payload)
        return message


class BotMessageViewExtended(ABCBotMessageViewExtended, BotMessageView):
    pass

