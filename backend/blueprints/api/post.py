from flask import request, session

from backend.blueprints.api.user import require_logged_in
from backend.constants import DATA
from backend.data.managers.PostMananger import (
    InvalidPostBody,
    InvalidPostTag,
    InvalidPostTitle,
    NoPostFoundError,
    PostAlreadyLockedError,
    PostManager,
    PostNotLockedError,
    RolePermissionError,
    TagLimitExceeded,
)
from backend.data.managers.SubForumManager import NoSubForumFoundError
from backend.data.managers.VoteManager import (
    ContentType,
    InvalidContent,
    InvalidContentType,
    NoVoteFoundError,
    VoteManager,
)
from backend.utils import make_blueprint, make_error, make_success, require_keys

blueprint = make_blueprint("post", __name__)


@blueprint.route("/create", methods=["POST"])
@require_keys(["subforum", "title", "body"])
@require_logged_in
def create():
    subforum = request.form.get("subforum")
    title = request.form.get("title")
    body = request.form.get("body")
    op = session[DATA.USER]["username"]

    # Optional
    media = request.form.get("media")
    tags = request.form.get("tags")

    post_manager = PostManager()
    try:
        created = post_manager.create_post(op, subforum, title, body, media, tags)
    except (
        InvalidPostTitle,
        InvalidPostBody,
        InvalidPostTag,
        TagLimitExceeded,
        NoSubForumFoundError,
    ) as e:
        return make_error(str(e), e=e)
    if not created:
        return make_error("Could not create")
    return make_success("Post created")


@blueprint.route("/delete", methods=["DELETE"])
@require_keys(["post_id"])
@require_logged_in
def delete():
    post_id = request.form.get("post_id")
    username = session[DATA.USER]["username"]

    post_manager = PostManager()
    try:
        deleted = post_manager.delete_post(username, post_id)
    except (RolePermissionError, NoPostFoundError) as e:
        return make_error(str(e), e=e)
    if not deleted:
        return make_error("Could not delete")

    return make_success("Post deleted")


@blueprint.route("/edit", methods=["POST"])
@require_keys(["post_id", "title", "body"])
@require_logged_in
def edit():
    post_id = request.form.get("post_id")
    title = request.form.get("title")
    body = request.form.get("body")
    media = request.form.get("media")
    tags = request.form.get("tags")
    username = session[DATA.USER]["username"]

    post_manager = PostManager()
    try:
        updated = post_manager.edit_post(username, post_id, title, body, media, tags)
    except (
        InvalidPostTitle,
        InvalidPostBody,
        InvalidPostTag,
        TagLimitExceeded,
        NoPostFoundError,
        RolePermissionError,
    ) as e:
        return make_error(str(e), e=e)
    if not updated:
        return make_error("Could not update post")

    return make_success("Post updated")


@blueprint.route("/lock", methods=["POST"])
@require_keys(["post_id"])
@require_logged_in
def lock():
    post_id = request.form.get("post_id")
    username = session[DATA.USER]["username"]

    post_manager = PostManager()

    try:
        locked = post_manager.lock_post(username, post_id)
    except (NoPostFoundError, PostAlreadyLockedError, RolePermissionError) as e:
        return make_error(str(e), e=e)
    if not locked:
        return make_error("Could not lock post")

    return make_success("Post locked")


@blueprint.route("/unlock", methods=["POST"])
@require_keys(["post_id"])
@require_logged_in
def unlock():
    post_id = request.form.get("post_id")
    username = session[DATA.USER]["username"]

    post_manager = PostManager()

    try:
        locked = post_manager.unlock_post(username, post_id)
    except (NoPostFoundError, PostNotLockedError, RolePermissionError) as e:
        return make_error(str(e), e=e)
    if not locked:
        return make_error("Could not unlock post")

    return make_success("Post unlocked")


@blueprint.route("/vote", methods=["POST"])
@require_keys(["post_id", "is_like"])
@require_logged_in
def vote():
    post_id = request.form.get("post_id")
    is_like = request.form.get("is_like", type=lambda s: s.lower() == "true")
    username = session[DATA.USER]["username"]

    vote_manager = VoteManager()

    try:
        added = vote_manager.add_vote(username, post_id, ContentType.POST, is_like)
    except (InvalidContentType, InvalidContent) as e:
        return make_error(str(e), e=e)
    if not added:
        return make_error("Could not add post vote")

    return make_success("Post vote ackowledged")


@blueprint.route("/unvote", methods=["POST"])
@require_keys(["post_id"])
@require_logged_in
def unvote():
    post_id = request.form.get("post_id")
    username = session[DATA.USER]["username"]

    vote_manager = VoteManager()

    try:
        removed = vote_manager.remove_vote(username, post_id, ContentType.POST)
    except (InvalidContentType, InvalidContent, NoVoteFoundError) as e:
        return make_error(str(e), e=e)
    if not removed:
        return make_error("Could not remove post vote")

    return make_success("Post vote removed")
