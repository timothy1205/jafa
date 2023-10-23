from abc import ABC, abstractmethod

from backend.data.models.PostModel import PostModel
from backend.data.models.SubForumModel import SubForumModel
from backend.data.models.UserModel import UserModel
from backend.data.models.VoteModel import VoteModel


class AbstractModelFactory(ABC):
    @staticmethod
    @abstractmethod
    def create_user_model() -> UserModel:
        """Create instance of UserModel"""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_subforum_model() -> SubForumModel:
        """Create instance of SubForumModel"""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def create_vote_model() -> VoteModel:
        """Create instance of VoteModel"""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def create_post_model() -> PostModel:
        """Create instance of PostModel"""
        raise NotImplementedError()
