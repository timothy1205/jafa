from abc import ABC, abstractmethod
from backend.data.models.UserModel import UserModel
from backend.data.models.SubForumModel import SubForumModel


class AbstractModelFactory:
    @staticmethod
    @abstractmethod
    def create_user_model() -> UserModel:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_subforum_model() -> SubForumModel:
        raise NotImplementedError()
