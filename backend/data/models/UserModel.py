from abc import ABC, abstractmethod
from typing import Optional, TypedDict
from datetime import date
from backend.data.models.Model import Model


class User(TypedDict):
    username: str
    password: str
    registration_date: date


class UserModel(ABC, Model):
    @abstractmethod
    def create_user(self, username: str, password: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, username: str) -> bool:
        raise NotImplementedError()
