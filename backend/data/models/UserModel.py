from abc import ABC, abstractmethod
from datetime import date
from typing import TypedDict

from backend.data.models.Model import Model


class User(TypedDict):
    username: str
    password: str
    registration_date: date


class UserModel(ABC, Model):
    @abstractmethod
    def create_user(self, data: User) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_by_username(self, username: str) -> User | None:
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, username: str) -> bool:
        raise NotImplementedError()
