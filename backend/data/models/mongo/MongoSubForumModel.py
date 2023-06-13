from typing import Optional
from datetime import datetime
from backend.data.models.SubForumModel import SubForumModel, SubForum
from backend.data.models.mongo.MongoMixin import MongoMixin

SUBFORUMS_COLLECTION = "subforums"


class MongoSubForumModel(MongoMixin, SubForumModel):
    def __init__(self):
        super().__init__()

    def __subforums_collection(self):
        return self._get_collection(SUBFORUMS_COLLECTION)

    def create_subforum(self, creator: str, title: str, description: str) -> bool:
        result = self.__subforums_collection().insert_one(
            {"creator": creator,
             "title": title,
             "description": description,
             "creation_date": datetime.now()})
        return result.acknowledged

    def delete_subforum(self, title: str) -> bool:
        result = self.__subforums_collection().delete_one({"title": title})
        return result.deleted_count != 0

    def edit_subforum(self, title: str, description: str) -> bool:
        result = self.__subforums_collection().update_one(
            {"title": title}, {"$set": {"description": description}})
        return result.modified_count != 0

    def get_by_title(self, title: str) -> Optional[SubForum]:
        subforum = self.__subforums_collection().find_one({"title": title})

        if subforum is None:
            return None

        return {"creator": subforum["creator"],
                "title": subforum["title"],
                "description": subforum["description"],
                "creation_date": subforum["creation_date"]}
