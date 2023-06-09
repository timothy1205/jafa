from abc import ABC, abstractmethod
from typing import Optional, TypedDict
from datetime import date
from backend.data.models.Model import Model


class SubForum(TypedDict):
    creator: str
    title: str
    description: str
    creation_date: date


class SubForumModel(ABC, Model):
    @abstractmethod
    def create_subforum(self, creator: str, title: str, description: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def delete_subforum(self, title: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def edit_subforum(self, title: str, description: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_by_title(self, title: str) -> Optional[SubForum]:
        raise NotImplementedError()
