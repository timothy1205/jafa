from abc import ABC, abstractmethod
from datetime import date
from enum import Enum
from typing import TypedDict

from backend.data.models.Model import Model


class ContentType(Enum):
    POST = 1
    COMMENT = 2


class BaseVote(TypedDict):
    username: str
    content_id: str
    content_type: ContentType


class Vote(BaseVote):
    is_like: bool
    creation_date: date


class VoteModel(ABC, Model):
    @abstractmethod
    def add_vote(self, data: Vote) -> bool:
        raise NotImplementedError()

    def get_vote(self, data: BaseVote) -> Vote | None:
        raise NotImplementedError()

    @abstractmethod
    def update_vote(self, data: Vote) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def remove_vote(self, data: BaseVote) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def clear_votes_by_username(self, username: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def clear_votes_by_id(self, content_id: str) -> bool:
        raise NotImplementedError()
