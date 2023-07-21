from typing import Optional
import json

from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.SubForumModel import SubForum, SubForumModel
from backend.data.models.UserModel import User, UserModel
from backend.data.models.PostModel import BasePost, CreatePost, Post, PostModel
from backend.data.models.VoteModel import BaseVote, Vote, VoteModel


class TestUserModel(UserModel):
    def __init__(self):
        self.db = {}

    def create_user(self, data: User) -> bool:
        self.db[data["username"]] = data
        return True

    def get_by_username(self, username) -> Optional[User]:
        return self.db.get(username)

    def delete_user(self, username) -> bool:
        del self.db[username]
        return True


class TestSubForumModel(SubForumModel):
    def __init__(self):
        self.db = {}

    def create_subforum(self, data: SubForum) -> bool:
        self.db[data["title"]] = data
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


class TestPostModel(PostModel):
    def __init__(self):
        self.db = {}

    def create_post(self, data: CreatePost) -> bool:
        post_id = str(len(self.db.keys()))
        self.db[post_id] = data
        return True

    def get_by_post_id(self, post_id: str) -> Post:
        return self.db.get(post_id)

    def delete_by_post_id(self, post_id: str) -> bool:
        del self.db[post_id]
        return True

    def clear_posts(self, username: str) -> bool:
        to_clear = []
        for item in self.db.items():
            key, post = item
            if post["username"] == username:
                to_clear.append(key)

        for key in to_clear:
            del self.db[key]

        return True

    def edit_post(self, post_id: str, data: BasePost) -> bool:
        self.db[post_id] = data
        return True

    def lock_post(self, post_id: str) -> bool:
        self.db[post_id]["locked"] = True
        return True

    def unlock_post(self, post_id: str) -> bool:
        self.db[post_id]["locked"] = False
        return True

    def get_post_list_by_time(self, limit: int = 0) -> list[Post]:
        return list(self.db.values())


class TestVoteModel(VoteModel):
    def __init__(self):
        self.db = {}

    def __hash(self, data):
        return hash(json.dumps(data, sort_keys=True))

    def add_vote(self, data: Vote) -> bool:
        base = dict(
            username=data["username"],
            content_id=data["content_id"],
            content_type=data["content_type"],
        )
        self.db[self.__hash(base)] = data
        return True

    def get_vote(self, data: BaseVote) -> Vote:
        return self.db.get(self.__hash(data))

    def update_vote(self, data: Vote) -> bool:
        return self.add_vote(data)

    def remove_vote(self, data: BaseVote) -> bool:
        base = dict(
            username=data["username"],
            content_id=data["content_id"],
            content_type=data["content_type"],
        )
        del self.db[self.__hash(base)]
        return True

    def clear_votes_by_username(self, username: str) -> bool:
        to_clear = []
        for item in self.db.items():
            key, vote = item
            if vote["username"] == username:
                to_clear.append(key)

        for key in to_clear:
            del self.db[key]

        return True

    def clear_votes_by_id(self, content_id: str) -> bool:
        to_clear = []
        for item in self.db.items():
            key, vote = item
            if vote["content_id"] == content_id:
                to_clear.append(key)

        for key in to_clear:
            del self.db[key]

        return True


class TestModelFactory(AbstractModelFactory):
    @staticmethod
    def reset():
        TestModelFactory._cache = dict(
            user=TestUserModel(),
            subforum=TestSubForumModel(),
            post=TestPostModel(),
            vote=TestVoteModel(),
        )

    @staticmethod
    def create_user_model() -> UserModel:
        return TestModelFactory._cache["user"]

    @staticmethod
    def create_subforum_model() -> SubForumModel:
        return TestModelFactory._cache["subforum"]

    @staticmethod
    def create_post_model() -> PostModel:
        return TestModelFactory._cache["post"]

    @staticmethod
    def create_vote_model() -> PostModel:
        return TestModelFactory._cache["vote"]
