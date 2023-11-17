from typing import Callable
import unittest
from flask import Flask, session
from backend.tests import setup_test_context
from backend.constants import DATA
from backend.data.managers.AbstractManagerFactory import AbstractManagerFactory
from backend.data.managers.PostMananger import PostManager
from backend.data.managers.SubForumManager import SubForumManager
from backend.data.managers.UserManager import UserManager
from backend.data.managers.VoteManager import VoteManager


class TestManagerFactory(AbstractManagerFactory):
    @staticmethod
    def create_post_manager() -> PostManager:  # NOSONAR
        pass

    @staticmethod
    def create_subforum_manager() -> SubForumManager:  # NOSONAR
        pass

    @staticmethod
    def create_user_manager() -> UserManager:  # NOSONAR
        pass

    @staticmethod
    def create_vote_manager() -> VoteManager:  # NOSONAR
        pass


def blueprint_test_success(
    tc: unittest.TestCase,
    app: Flask,
    run: Callable,
    request_data: dict | None,
    manager: any,
    manager_method: str,
    success_msg: str,
):
    """Test for a successful response from a bluerpint route"""
    with tc.subTest("Success"):

        def test():
            # Set user as logged in
            session[DATA.USER] = dict(username="")

            # Override method with catch-all function to always return True
            old_method = getattr(manager, manager_method)
            setattr(manager, manager_method, lambda *args, **kwargs: True)

            # Assert output
            expected_response = dict(msg=success_msg)
            response = run().get_json()
            tc.assertEqual(response, expected_response)

            # Restore previous method
            setattr(manager, manager_method, old_method)

        setup_test_context(app, test, request_data)


def blueprint_test_fail(
    tc: unittest.TestCase,
    app: Flask,
    run: Callable,
    request_data: dict | None,
    manager: any,
    manager_method: str,
    fail_msg: str,
):
    """Test for a failed response (without any exceptions raised) from a bluerpint route"""
    with tc.subTest("Fail without raising"):

        def test():
            # Set user as logged in
            session[DATA.USER] = dict(username="")

            # Override method with catch-all function to always return False
            old_method = getattr(manager, manager_method)
            setattr(manager, manager_method, lambda *args, **kwargs: False)

            # Assert output
            expected_response = dict(type="ActionFailed", error=fail_msg)
            response = run().get_json()
            tc.assertEqual(response, expected_response)

            # Restore previous method
            setattr(manager, manager_method, old_method)

        setup_test_context(app, test, request_data)


def blueprint_test_raise(
    tc: unittest.TestCase,
    app: Flask,
    run: Callable,
    request_data: dict | None,
    manager: any,
    manager_method: str,
    exception_types: list[type],
):
    """Test that a blueprint route catches given exceptions."""
    for t in exception_types:
        e = t()
        with tc.subTest(f"{e.__class__.__name__} is caught"):

            def test(e=e):
                # Set user as logged in
                session[DATA.USER] = dict(username=str)

                # Define catch-all function to always raise current exception
                def raise_e(*args, **kwargs):
                    raise e

                # Override method with raise_e
                old_method = getattr(manager, manager_method)
                setattr(manager, manager_method, raise_e)

                try:
                    response = run().get_json()
                except Exception:
                    tc.fail("Exception was not caught")

                # Check error type
                tc.assertIn("type", response)
                tc.assertEqual(e.__class__.__name__, response["type"])

                # Ensure that error exists as a string in message.
                # We don't care what it is.
                tc.assertIn("error", response)
                tc.assertIsInstance(response["error"], str)

                setattr(manager, manager_method, old_method)

            setup_test_context(
                app,
                test,
                request_data,
            )
