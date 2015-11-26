import unittest
import time

from accessors.routes import bus_route_accessor, busway_transfer_accessor, train_route_accessor
from fetcher import busway_transfer_fetcher, train_info_fetcher
import fetcher.busway_info_fetcher


class FetcherTest(unittest.TestCase):
    def test_transporation_fetcher(self):
        bus_route_accessor.reset()
        fetcher.busway_info_fetcher.start()
        routes = bus_route_accessor.get_all_bus_routes()
        self.assertIsNotNone(routes)
        self.assertTrue(len(routes) > 0)
        fetcher.busway_info_fetcher.stop()

    def test_transfer_fetcher(self):
        busway_transfer_accessor.reset()
        busway_transfer_fetcher.start()
        routes = busway_transfer_accessor.get_all_busway_transfers()
        self.assertIsNotNone(routes)
        self.assertTrue(len(routes) > 0)
        busway_transfer_fetcher.stop()

    def test_train_fetcher(self):
        train_route_accessor.reset()
        train_info_fetcher.start()
        routes = train_route_accessor.get_all_train_routes()
        self.assertIsNotNone(routes)
        self.assertTrue(len(routes) > 0)

    def runTest(self):
        self.test_transporation_fetcher()
