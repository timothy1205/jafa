from typing import Optional
from bson.errors import InvalidId
from bson.objectid import ObjectId

from backend.data.models.mongo.MongoMixin import MongoMixin
from backend.data.models.VoteModel import BaseVote, Vote, VoteModel

VOTES_COLLECTION = "votes"


class MongoVoteModel(MongoMixin, VoteModel):
    def __init__(self):
        super().__init__()

    def add_vote(self, data: Vote) -> bool:
        try:
            result = self._get_collection(VOTES_COLLECTION).insert_one(
                dict(
                    username=data["username"],
                    content_id=ObjectId(data["content_id"]),
                    content_type=data["content_type"],
                    is_like=data["is_like"],
                    creation_date=data["creation_date"],
                )
            )
        except InvalidId:
            return False

        return result.acknowledged

    def get_vote(self, data: BaseVote) -> Optional[Vote]:
        try:
            vote = self._get_collection(VOTES_COLLECTION).find_one(
                dict(
                    username=data["username"],
                    content_id=ObjectId(data["content_id"]),
                    content_type=data["content_type"],
                )
            )
        except InvalidId:
            return None

        if vote is None:
            return None

        return dict(
            username=vote["username"],
            content_id=str(vote["content_id"]),
            content_type=vote["content_type"],
            is_like=vote["is_like"],
            creation_date=vote["creation_date"],
        )

    def update_vote(self, data: Vote) -> bool:
        try:
            result = self._get_collection(VOTES_COLLECTION).update_one(
                dict(
                    username=data["username"],
                    content_id=ObjectId(data["content_id"]),
                    content_type=data["content_type"],
                ),
                {
                    "$set": dict(
                        is_like=data["is_like"],
                        creation_date=data["creation_date"],
                    )
                },
            )
        except InvalidId:
            return False

        return result.modified_count != 0

    def remove_vote(self, data: BaseVote) -> bool:
        try:
            result = self._get_collection(VOTES_COLLECTION).delete_one(
                dict(
                    username=data["username"],
                    content_id=ObjectId(data["content_id"]),
                    content_type=data["content_type"],
                )
            )
        except InvalidId:
            return False

        return result.deleted_count != 0

    def clear_votes_by_username(self, username: str) -> bool:
        result = self._get_collection(VOTES_COLLECTION).delete_many(
            dict(username=username)
        )
        return result.acknowledged

    def clear_votes_by_id(self, content_id: str) -> bool:
        try:
            result = self._get_collection(VOTES_COLLECTION).delete_many(
                dict(content_id=ObjectId(content_id))
            )
        except InvalidId:
            return False

        return result.acknowledged
