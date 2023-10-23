from backend.data.models.AbstractModelFactory import AbstractModelFactory
from typing import Dict
from backend.data.models.PostModel import PostModel
from backend.data.models.SubForumModel import SubForumModel

from backend.data.models.UserModel import UserModel
from backend.data.models.VoteModel import VoteModel


class TestModelFactory(AbstractModelFactory):
    @staticmethod
    def create_user_model() -> UserModel:  # NOSONAR
        pass

    @staticmethod
    def create_subforum_model() -> SubForumModel:  # NOSONAR
        pass

    @staticmethod
    def create_vote_model() -> VoteModel:  # NOSONAR
        pass

    @staticmethod
    def create_post_model() -> PostModel:  # NOSONAR
        pass
