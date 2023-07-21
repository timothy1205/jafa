from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, TypedDict

from backend.data.models.Model import Model


class BasePost(TypedDict):
    op: str
    title: str
    body: str
    media: Optional[list[str]]
    tags: Optional[list[str]]
    modified_date: Optional[date]
    likes: int
    dislikes: int


class CreatePost(BasePost):
    subforum: str
    creation_date: date
    locked: bool


class Post(CreatePost):
    post_id: str


class PostModel(ABC, Model):
    @abstractmethod
    def create_post(self, data: CreatePost) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_by_post_id(self, post_id: str) -> Optional[Post]:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_post_id(self, post_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def clear_posts(self, username: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def edit_post(self, post_id: str, data: BasePost) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def lock_post(self, post_id: str) -> bool:
        raise NotImplementedError()

    def unlock_post(self, post_id: str) -> bool:
        raise NotImplementedError()

    def get_post_list_by_time(self, subforum: str) -> list[Post]:
        raise NotImplementedError()
