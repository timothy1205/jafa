from typing import Optional
from datetime import datetime
from backend.data.models.UserModel import UserModel, User
from backend.data.models.mongo.MongoMixin import MongoMixin

USERS_COLLECTION = "users"


class MongoUserModel(MongoMixin, UserModel):
    def __init__(self):
        super().__init__()

    def create_user(self, username: str, password: str) -> bool:
        return self._get_collection(USERS_COLLECTION).insert_one({"username": username,
                                                                  "password": password,
                                                                  "registration_date": datetime.now()})

    def get_by_username(self, username: str) -> Optional[User]:
        user = self._get_collection(
            USERS_COLLECTION).find_one({"username": username})

        if user is None:
            return None

        return {"username": user["username"],
                "password": user["password"],
                "registration_date": user["registration_date"]}

    def delete_user(self, username) -> bool:
        result = self._get_collection(
            USERS_COLLECTION).delete_one({"username": username})
        return result.deleted_count != 0
