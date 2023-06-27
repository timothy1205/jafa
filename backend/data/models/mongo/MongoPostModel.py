from typing import Optional

from bson.objectid import ObjectId

from backend.data.models.mongo.MongoMixin import MongoMixin
from backend.data.models.PostModel import BasePost, CreatePost, Post, PostModel

POSTS_COLLECTION = "posts"


class MongoPostModel(MongoMixin, PostModel):
    def __init__(self):
        super().__init__()

    def __posts_collection(self):
        return self._get_collection(POSTS_COLLECTION)

    def create_post(self, data: CreatePost) -> bool:
        result = self.__posts_collection().insert_one(
            dict(
                op=data["op"],
                title=data["title"],
                body=data["body"],
                media=data["media"],
                tags=data["tags"],
                creation_date=data["creation_date"],
                locked=data["locked"],
                modified_date=data["modified_date"],
            )
        )

        return result.acknowledged

    def get_by_post_id(self, post_id: str) -> Optional[Post]:
        post = self.__posts_collection().find_one({"_id": ObjectId(post_id)})

        if post is None:
            return None

        return dict(
            op=post["op"],
            title=post["title"],
            body=post["body"],
            media=post["media"],
            tags=post["tags"],
            creation_data=post["creation_date"],
            locked=post["locked"],
            post_id=str(post["_id"]),
            modified_date=post["modified_date"],
        )

    def delete_by_post_id(self, post_id: str) -> bool:
        result = self.__posts_collection().delete_one({"_id": ObjectId(post_id)})

        return result.deleted_count != 0

    def clear_posts(self, username: str) -> bool:
        result = self.__posts_collection().delete_many({"username": username})

        return result.acknowledged

    def edit_post(self, post_id: str, data: BasePost) -> bool:
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
                )
            },
        )

        return result.modified_count != 0

    def lock_post(self, post_id: str) -> bool:
        result = self.__posts_collection().update_one(
            {"_id": ObjectId(post_id)}, {"$set": dict(locked=True)}
        )

        return result.modified_count != 0

    def unlock_post(self, post_id: str) -> bool:
        result = self.__posts_collection().update_one(
            {"_id": ObjectId(post_id)}, {"$set": dict(locked=False)}
        )

        return result.modified_count != 0
