from typing import Optional

from bson.errors import InvalidId
from bson.objectid import ObjectId

from backend.data.models.mongo.MongoMixin import MongoMixin
from backend.data.models.PostModel import BasePost, CreatePost, Post, PostModel

POSTS_COLLECTION = "posts"


class MongoPostModel(MongoMixin, PostModel):
    def __init__(self):
        super().__init__()

    def __posts_collection(self):
        return self._get_collection(POSTS_COLLECTION)

    def __filter_post_result(self, post):
        data = dict(post)

        # Format _id
        del data["_id"]
        data["post_id"] = str(post["_id"])

        return data

    def create_post(self, data: CreatePost) -> bool:
        result = self.__posts_collection().insert_one(dict(data))

        return result.acknowledged

    def get_by_post_id(self, post_id: str) -> Optional[Post]:
        try:
            post = self.__posts_collection().find_one({"_id": ObjectId(post_id)})
        except InvalidId:
            return None

        if post is None:
            return None

        return self.__filter_post_result(post)

    def delete_by_post_id(self, post_id: str) -> bool:
        try:
            result = self.__posts_collection().delete_one({"_id": ObjectId(post_id)})
        except InvalidId:
            return False

        return result.deleted_count != 0

    def clear_posts(self, username: str) -> bool:
        result = self.__posts_collection().delete_many({"username": username})

        return result.acknowledged

    def edit_post(self, post_id: str, data: BasePost) -> bool:
        try:
            result = self.__posts_collection().update_one(
                {"_id": ObjectId(post_id)},
                {
                    "$set": dict(
                        op=data["op"],
                        title=data["title"],
                        body=data["body"],
                        media=data["media"],
                        tags=data["tags"],
                        modified_date=data["modified_date"],
                        likes=data["likes"],
                        dislikes=data["dislikes"],
                    )
                },
            )
        except InvalidId:
            return False

        return result.modified_count != 0

    def lock_post(self, post_id: str) -> bool:
        try:
            result = self.__posts_collection().update_one(
                {"_id": ObjectId(post_id)}, {"$set": dict(locked=True)}
            )
        except InvalidId:
            return False

        return result.modified_count != 0

    def unlock_post(self, post_id: str) -> bool:
        try:
            result = self.__posts_collection().update_one(
                {"_id": ObjectId(post_id)}, {"$set": dict(locked=False)}
            )
        except InvalidId:
            return False

        return result.modified_count != 0

    def get_post_list_by_time(self, subforum: str) -> list[Post]:
        results = (
            self.__posts_collection().find({"subforum": subforum}).sort("creation_date")
        )

        filtered = map(self.__filter_post_result, results)

        return list(filtered)
