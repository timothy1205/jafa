from typing import Optional

from backend.data.models.mongo.MongoMixin import MongoMixin
from backend.data.models.UserModel import User, UserModel

USERS_COLLECTION = "users"


class MongoUserModel(MongoMixin, UserModel):
    def __init__(self):
        super().__init__()

    def create_user(self, data: User) -> bool:
        return self._get_collection(USERS_COLLECTION).insert_one(
            {
                "username": data["username"],
                "password": data["password"],
                "registration_date": data["registration_date"],
            }
        )

    def get_user_by_username(self, username: str) -> Optional[User]:
        user = self._get_collection(USERS_COLLECTION).find_one({"username": username})

        if user is None:
            return None

        return {
            "username": user["username"],
            "password": user["password"],
            "registration_date": user["registration_date"],
        }

    def delete_user(self, username) -> bool:
        # Delete user document
        user = self._get_collection(USERS_COLLECTION).delete_one({"username": username})

        return user.deleted_count != 0
