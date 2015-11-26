import logging
import unittest

from test.AccessorTest import AccessorTest
from test.FetcherTest import FetcherTest
from test.ServiceTest import ServiceTest

if __name__ == '__main__':
    runner = unittest.TextTestRunner()

    test_suite = unittest.TestSuite()
    test_suite.addTest(AccessorTest())
    test_suite.addTest(ServiceTest())
    test_suite.addTest(FetcherTest())
    runner.run(test_suite)
