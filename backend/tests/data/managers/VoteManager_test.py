import sys
import unittest

import backend.data.managers.VoteManager as vm
from backend.data.managers.PostMananger import PostManager
from backend.data.managers.SubForumManager import SubForumManager
from backend.tests.data.models.TestModelFactory import TestModelFactory


class VoteManagerTestCase(unittest.TestCase):
    def setUp(self):
        TestModelFactory.reset()
        self.vote_model = TestModelFactory.create_vote_model()
        self.vote_manager = vm.VoteManager(TestModelFactory)

        # Default subforum to use
        subforum_manager = SubForumManager(TestModelFactory)
        subforum_manager.create_subforum("test", "test", "Test Description")

        # Default post
        self.post_manager = PostManager(TestModelFactory)
        self.post_manager.create_post("test", "test", "Test Post", "Test Message")

    def test_add_vote(self):
        # Posts
        with self.assertRaises(vm.InvalidContent, msg="Invalid post"):
            self.vote_manager.add_vote("test", "random", vm.ContentType.POST, True)

        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, True), "Valid"
        )
        self.assertEqual(self.post_manager.get_post("0")["likes"], 1, "Post updated")

        self.setUp()

        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, False), "Valid"
        )
        self.assertEqual(self.post_manager.get_post("0")["dislikes"], 1, "Post updated")

        self.setUp()

        ## Update a vote from a like to dislike
        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, True), "Valid"
        )
        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, False), "Valid"
        )
        self.assertEqual(
            self.post_manager.get_post("0")["dislikes"], 1, "Dislike counted"
        )
        self.assertEqual(self.post_manager.get_post("0")["likes"], 0, "Like reset")
        self.assertEqual(len(self.vote_model.db.keys()), 1, "One vote created")

        self.setUp()

        ## Update a vote from a dislike to like
        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, False), "Valid"
        )
        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, True), "Valid"
        )
        self.assertEqual(self.post_manager.get_post("0")["likes"], 1, "Like counted")
        self.assertEqual(
            self.post_manager.get_post("0")["dislikes"], 0, "Dislike reset"
        )
        self.assertEqual(len(self.vote_model.db.keys()), 1, "One vote created")

        self.setUp()

        ## Update a vote from a like to like
        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, False), "Valid"
        )
        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, True), "Valid"
        )
        self.assertEqual(self.post_manager.get_post("0")["likes"], 1, "Like counted")
        self.assertEqual(self.post_manager.get_post("0")["dislikes"], 0, "Dislike is 0")
        self.assertEqual(len(self.vote_model.db.keys()), 1, "One vote created")

        self.setUp()

        ## Update a vote from a dislike to dislike
        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, False), "Valid"
        )
        self.assertTrue(
            self.vote_manager.add_vote("test", "0", vm.ContentType.POST, False), "Valid"
        )
        self.assertEqual(
            self.post_manager.get_post("0")["dislikes"], 1, "Dislike counted"
        )
        self.assertEqual(self.post_manager.get_post("0")["likes"], 0, "Like is 0")
        self.assertEqual(len(self.vote_model.db.keys()), 1, "One vote created")

    def test_remove_vote(self):
        # Posts
        with self.assertRaises(vm.NoVoteFoundError, msg="Invalid vote"):
            self.vote_manager.remove_vote("random", "random", vm.ContentType.POST)

        self.vote_manager.add_vote("test", "0", vm.ContentType.POST, True)
        self.assertTrue(self.vote_manager.remove_vote("test", "0", vm.ContentType.POST))

    def test_clear_votes_by_id(self):
        # Contains no logic
        pass
