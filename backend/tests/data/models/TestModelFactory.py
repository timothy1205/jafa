from typing import Optional
from datetime import datetime
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.UserModel import UserModel, User
from backend.data.models.SubForumModel import SubForumModel, SubForum


class TestUserModel(UserModel):
    def __init__(self):
        self.db = {}

    def create_user(self, username, password) -> bool:
        self.db[username] = dict(
            username=username,
            password=password,
            registration_date=datetime.now())
        return True

    def get_user_by_username(self, username) -> Optional[User]:
        return self.db.get(username)

    def delete_user(self, username) -> bool:
        del self.db[username]
        return True


class TestSubForumModel(SubForumModel):
    def __init__(self):
        self.db = {}

    def create_subforum(self, creator, title, description) -> bool:
        self.db[title] = dict(
            creator=creator,
            title=title,
            description=description,
            creation_date=datetime.now())
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
            user=TestUserModel(), subforum=TestSubForumModel())

    @staticmethod
    def create_user_model() -> UserModel:
        return TestModelFactory._cache["user"]

    @staticmethod
    def create_subforum_model() -> SubForumModel:
        return TestModelFactory._cache["subforum"]
