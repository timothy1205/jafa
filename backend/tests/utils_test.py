import unittest
from backend.constants import HTTP
from backend.tests import setup_test_context
from backend.app import create_app

from backend.utils import (
    ceil_division,
    make_blueprint,
    make_error,
    make_success,
    require_keys,
)


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

    def test_make_error(self):
        with self.subTest("Test defaults"):

            def test():
                expected_response = dict(type="ActionFailed", error="Test")
                response = make_error("Test")
                response_json = response.get_json()

                self.assertEqual(
                    response.headers.get("Content-Type"), "application/json"
                )
                self.assertEqual(response.status_code, HTTP.BAD_REQUEST)
                self.assertEqual(expected_response, response_json)

            setup_test_context(self.app, test)

        with self.subTest("Test with all parameters"):

            def test():
                class TestException(Exception):
                    pass

                expected_response = dict(type="TestException", error="Test")
                response = make_error("Test", 500, TestException())
                response_json = response.get_json()

                self.assertEqual(
                    response.headers.get("Content-Type"), "application/json"
                )
                self.assertEqual(response.status_code, 500)
                self.assertEqual(expected_response, response_json)

            setup_test_context(self.app, test)

    def test_make_success(self):
        with self.subTest("Test with string mesage"):

            def test():
                expected_response = dict(msg="Test")
                response = make_success("Test")
                response_json = response.get_json()

                self.assertEqual(
                    response.headers.get("Content-Type"), "application/json"
                )
                self.assertEqual(response.status_code, HTTP.SUCCESS)
                self.assertEqual(expected_response, response_json)

            setup_test_context(self.app, test)

        with self.subTest("Test with custom dict"):

            def test():
                expected_response = dict(data="Test", data2="Test2", data3="Test3")
                response = make_success(dict(data="Test", data2="Test2", data3="Test3"))
                response_json = response.get_json()

                self.assertEqual(
                    response.headers.get("Content-Type"), "application/json"
                )
                self.assertEqual(response.status_code, HTTP.SUCCESS)
                self.assertEqual(expected_response, response_json)

            setup_test_context(self.app, test)

    def test_require_keys(self):
        with self.subTest("Empty list should never fail"):

            def test():
                @require_keys([])
                def blank():
                    pass

                self.assertIsNone(blank())

            setup_test_context(self.app, test)

        with self.subTest("Missing first key"):

            def test():
                @require_keys(["first", "second", "third"])
                def blank():
                    pass

                expected_response = dict(
                    type="MissingKeysError", error="Missing: ['first']"
                )
                response = blank()
                response_json = response.get_json()

                self.assertEqual(
                    response.headers.get("Content-Type"), "application/json"
                )
                self.assertEqual(response.status_code, HTTP.BAD_REQUEST)
                self.assertEqual(expected_response, response_json)

            setup_test_context(self.app, test, dict(second="2", third="3"))

        with self.subTest("Missing last key"):

            def test():
                @require_keys(["first", "second", "third"])
                def blank():
                    pass

                expected_response = dict(
                    type="MissingKeysError", error="Missing: ['third']"
                )
                response = blank()
                response_json = response.get_json()

                self.assertEqual(
                    response.headers.get("Content-Type"), "application/json"
                )
                self.assertEqual(response.status_code, HTTP.BAD_REQUEST)
                self.assertEqual(expected_response, response_json)

            setup_test_context(self.app, test, dict(first="1", second="2"))

        with self.subTest("Missing all keys"):

            def test():
                @require_keys(["first", "second", "third"])
                def blank():
                    pass

                expected_response = dict(
                    type="MissingKeysError",
                    error="Missing: ['first', 'second', 'third']",
                )
                response = blank()
                response_json = response.get_json()

                self.assertEqual(
                    response.headers.get("Content-Type"), "application/json"
                )
                self.assertEqual(response.status_code, HTTP.BAD_REQUEST)
                self.assertEqual(expected_response, response_json)

            setup_test_context(self.app, test)

        with self.subTest("Missing keys in response are sorted alphabetically"):

            def test():
                @require_keys(["third", "first", "second"])
                def blank():
                    pass

                expected_response = dict(
                    type="MissingKeysError",
                    error="Missing: ['first', 'second', 'third']",
                )
                response = blank()
                response_json = response.get_json()

                self.assertEqual(
                    response.headers.get("Content-Type"), "application/json"
                )
                self.assertEqual(response.status_code, HTTP.BAD_REQUEST)
                self.assertEqual(expected_response, response_json)

            setup_test_context(self.app, test)

        with self.subTest("All keys present"):

            def test():
                @require_keys(["first", "second", "third"])
                def blank():
                    pass

                self.assertIsNone(blank())

            setup_test_context(self.app, test, dict(first="1", second="2", third="3"))

    def test_ceil_division(self):
        self.assertEqual(1, ceil_division(1, 3))
        self.assertEqual(77, ceil_division(1481237419283, 19328718923))
        self.assertEqual(0, ceil_division(0, 1102301283))
        with self.assertRaises(ZeroDivisionError):
            ceil_division(1242891, 0)
        self.assertEqual(-76, ceil_division(-1481237419283, 19328718923))
        self.assertEqual(-76, ceil_division(1481237419283, -19328718923))
        self.assertEqual(77, ceil_division(-1481237419283, -19328718923))

    def test_make_blueprint(self):
        with self.subTest("Empty url_prefix becomes /name"):
            blueprint = make_blueprint("name", "import_name", url_prefix=None)

            self.assertEqual(blueprint.name, "name")
            self.assertEqual(blueprint.import_name, "import_name")
            self.assertEqual(blueprint.url_prefix, "/name")

        with self.subTest("Non-empty url_prefix is not overriden"):
            blueprint = make_blueprint("name", "import_name", url_prefix="/custom")

            self.assertEqual(blueprint.name, "name")
            self.assertEqual(blueprint.import_name, "import_name")
            self.assertEqual(blueprint.url_prefix, "/custom")
