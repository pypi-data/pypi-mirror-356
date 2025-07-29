import unittest

import numpy


def assert_allclose(self, actual, expected, rtol=1e-5, atol=1e-7):
    return numpy.testing.assert_allclose(actual, expected, rtol=rtol, atol=atol)
unittest.TestCase.assertAllClose = assert_allclose
