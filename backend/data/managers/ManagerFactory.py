from backend.data.managers.AbstractManagerFactory import AbstractManagerFactory
from backend.data.managers.PostMananger import PostManager
from backend.data.managers.SubForumManager import SubForumManager
from backend.data.managers.UserManager import UserManager
from backend.data.managers.VoteManager import VoteManager


class ManagerFactory(AbstractManagerFactory):
    @staticmethod
    def create_post_manager() -> PostManager:
        return PostManager()

    @staticmethod
    def create_subforum_manager() -> SubForumManager:
        return SubForumManager()

    @staticmethod
    def create_user_manager() -> UserManager:
        return UserManager()

    @staticmethod
    def create_vote_manager() -> VoteManager:
        return VoteManager()
