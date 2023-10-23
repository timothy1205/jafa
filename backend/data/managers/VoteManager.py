from datetime import datetime
from typing import Optional, Type

from backend.data.managers.AbstractDataManager import AbstractDataManager
from backend.data.models.AbstractModelFactory import AbstractModelFactory
from backend.data.models.VoteModel import ContentType, Vote


class NoVoteFoundError(Exception):
    pass


class InvalidContentType(Exception):
    pass


class InvalidContent(Exception):
    pass


CONTENT_TYPES = ["post", "comment"]


class VoteManager(AbstractDataManager):
    def __init__(self, model_factory: Optional[Type[AbstractModelFactory]] = None):
        super().__init__(model_factory)

    def __raise_or_return(self, vote):
        if vote is None:
            raise NoVoteFoundError("A vote with that ID and type does not exist")

        return vote

    def get_vote(
        self, username: str, content_id: str, content_type: ContentType
    ) -> Vote:
        """Return post with specified id

        :raises NoVoteFoundError:
        :raises InvalidContentType:
        """
        vote_model = self.model_factory.create_vote_model()

        vote = vote_model.get_vote(
            dict(
                username=username,
                content_id=content_id,
                content_type=str(content_type),
            )
        )

        if vote is not None:
            # Parse content_type
            found = False

            for current_type in ContentType:
                if vote["content_type"] == str(current_type):
                    vote["content_type"] = current_type
                    found = True
                    break

            if not found:
                raise InvalidContentType(
                    f"Cound not parse: {str(vote['content_type'])} {type(vote['content_type'])}"
                )

        return self.__raise_or_return(vote)

    def add_vote(
        self,
        username: str,
        content_id: str,
        content_type: ContentType,
        is_like: bool,
    ):
        """Create a user vote for some content (or update if exists)

        :returns: True if successful, false otherwise.
        :raises InvalidContent:
        :raises InvalidContentType:
        """
        from backend.data.managers.PostMananger import PostManager

        post_manager = PostManager(self.model_factory)

        if content_type == ContentType.POST:
            if not post_manager.post_exists(content_id):
                raise InvalidContent("Invalid post given")

        elif content_type == ContentType.COMMENT:
            # TODO: Check if comment exists
            pass
        else:
            # Should be unreachable
            raise InvalidContentType("Unknown content type: " + str(content_type))

        vote_model = self.model_factory.create_vote_model()

        try:
            vote = self.get_vote(username, content_id, content_type)
        except NoVoteFoundError:
            if content_type == ContentType.POST:
                # Update post likes
                post_manager.add_like(content_id, is_like)
            elif content_type == ContentType.COMMENT:
                # TODO: Update comment likes
                pass
            else:
                # Unreachable code
                pass

            # Create new vote
            return vote_model.add_vote(
                dict(
                    username=username,
                    content_id=content_id,
                    content_type=str(content_type),
                    is_like=is_like,
                    creation_date=datetime.now(),
                )
            )

        # No exception raised, update existing vote
        if vote["is_like"] != is_like:
            # If is_like is changing, update counts

            if content_type == ContentType.POST:
                # Update post likes
                post_manager.add_like(content_id, is_like)
                post_manager.add_like(content_id, vote["is_like"], False)
            elif content_type == ContentType.COMMENT:
                # TODO: Update comment likes
                pass
            else:
                # Unreachable code
                pass

        return vote_model.update_vote(
            dict(
                username=username,
                content_id=content_id,
                content_type=str(content_type),
                is_like=is_like,
                creation_date=datetime.now(),
            )
        )

    def remove_vote(self, username: str, content_id: str, content_type: ContentType):
        """Remove a user vote for some content

        :returns: True if successful, false otherwise.
        :raises NoVoteFoundError:
        :raises InvalidContentType:
        :raises InvalidContent:
        """
        vote = self.get_vote(username, content_id, content_type)

        if content_type == ContentType.POST:
            from backend.data.managers.PostMananger import PostManager

            post_manager = PostManager(self.model_factory)
            if not post_manager.post_exists(content_id):
                raise InvalidContent("Invalid post given")

            # Update post like/dislike counts
            post_manager.add_like(content_id, vote["is_like"], False)
        elif content_type == ContentType.COMMENT:
            # TODO: Check if comment exists
            pass
        else:
            # This should be unreachable due to checks in get_vote
            raise InvalidContentType("Unknown content type: " + str(content_type))

        vote_model = self.model_factory.create_vote_model()

        return vote_model.remove_vote(
            dict(
                username=username, content_id=content_id, content_type=str(content_type)
            )
        )

    def clear_votes_by_id(self, content_id: str):
        """Remove all votes associated with content_id

        :returns: True if successful, false otherwise.
        """
        vote_model = self.model_factory.create_vote_model()

        return vote_model.clear_votes_by_id(content_id)
