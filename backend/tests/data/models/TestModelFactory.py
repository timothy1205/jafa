from typing import Optional

from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.SubForumModel import SubForum, SubForumModel
from backend.data.models.UserModel import User, UserModel


class TestUserModel(UserModel):
    def __init__(self):
        self.db = {}

    def create_user(self, data: User) -> bool:
        self.db[username] = dict(
            username=data["username"],
            password=["password"],
            registration_date=data["registration_date"],
        )
        return True

    def get_user_by_username(self, username) -> Optional[User]:
        return self.db.get(username)

    def delete_user(self, username) -> bool:
        del self.db[username]
        return True


class TestSubForumModel(SubForumModel):
    def __init__(self):
        self.db = {}

    def create_subforum(self, data: SubForum) -> bool:
        self.db[title] = dict(
            creator=data["creator"],
            title=data["title"],
            description=data["description"],
            creation_date=data["creation_date"],
        )
        return True

    def delete_subforum(self, title) -> bool:
        del self.db[title]
        return True

    def edit_subforum(self, title, description) -> bool:
        if title not in self.db:
            return False

        self.db[title]["description"] = description
        return True

    def get_subforum_by_title(self, title) -> Optional[SubForumModel]:
        return self.db.get(title)


class TestModelFactory(AbstractModelFactory):
    @staticmethod
    def reset():
        TestModelFactory._cache = dict(
            user=TestUserModel(), subforum=TestSubForumModel()
        )

    @staticmethod
    def create_user_model() -> UserModel:
        return TestModelFactory._cache["user"]

    @staticmethod
    def create_subforum_model() -> SubForumModel:
        return TestModelFactory._cache["subforum"]
