from datetime import datetime, timedelta
import unittest


def assertTimeInRange(  # NOSONAR
    test_case: unittest.TestCase, time: datetime, seconds=1, msg=None
):
    test_case.assertAlmostEqual(
        datetime.now(), time, delta=timedelta(seconds=seconds), msg=msg
    )
