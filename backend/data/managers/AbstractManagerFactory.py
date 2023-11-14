from abc import ABC, abstractmethod

from backend.data.managers import SubForumManager, UserManager, VoteManager
from backend.data.managers.PostMananger import PostManager


class AbstractManagerFactory(ABC):
    """Generate manager objects through static methods.

    The purpose of this class is soley to allow for dependency injection.
    As a result, abstract classes of each the manager classes are not defined.
    """

    @abstractmethod
    def create_post_manager(self) -> PostManager:
        raise NotImplementedError()

    @abstractmethod
    def create_subforum_manager(self) -> SubForumManager:
        raise NotImplementedError()

    @abstractmethod
    def create_user_manager(self) -> UserManager:
        raise NotImplementedError()

    @abstractmethod
    def create_vote_manager(self) -> VoteManager:
        raise NotImplementedError()
