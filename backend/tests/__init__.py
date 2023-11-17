import unittest
from datetime import datetime, timedelta
from typing import Callable

from flask import Flask


def assertTimeInRange(  # NOSONAR
    test_case: unittest.TestCase, time: datetime, seconds=1, msg=None
):
    test_case.assertAlmostEqual(
        datetime.now(), time, delta=timedelta(seconds=seconds), msg=msg
    )


def setup_test_context(app: Flask, f: Callable, data: dict | None = None):
    """Wrapper function for test_request_context"""
    with app.test_request_context(data=data):
        f()


def set_data_wrapper(data: dict):
    """Return a set_data function with that updates the given data dict."""
    data["args"] = None
    data["kwargs"] = None

    def set_data(*args, **kwargs):
        data["args"] = args
        data["kwargs"] = kwargs

    return set_data
