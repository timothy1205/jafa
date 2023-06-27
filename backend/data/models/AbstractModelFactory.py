from abc import ABC, abstractmethod
from backend.data.models.UserModel import UserModel
from backend.data.models.SubForumModel import SubForumModel
from backend.data.models.VoteModel import VoteModel
from backend.data.models.PostModel import PostModel


class AbstractModelFactory:
    @staticmethod
    @abstractmethod
    def create_user_model() -> UserModel:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_subforum_model() -> SubForumModel:
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_vote_model() -> VoteModel:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_post_model() -> PostModel:
        raise NotImplementedError()
