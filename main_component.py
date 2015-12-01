from accessors import bus_estimation_accessor
from config import general_config
from accessors.routes import bus_route_accessor
from common.logging import logger_factory
from fetcher import busway_info_fetcher, busway_track_fetcher, train_info_fetcher, walk_info_fetcher, \
    busway_transfer_fetcher
from services import autocomplete_service, search_service

__logger = logger_factory.create_logger(__name__)


def start():
    # warming up
    __logger.info('System is warming up')
    bus_estimation_accessor.start()
    busway_info_fetcher.start()
    train_info_fetcher.start()
    walk_info_fetcher.start()
    busway_transfer_fetcher.start()
    busway_track_fetcher.start()
    autocomplete_service.start()
    __logger.info('All components have been started')


def stop():
    bus_estimation_accessor.stop()
    busway_info_fetcher.stop()
    train_info_fetcher.stop()
    walk_info_fetcher.stop()
    busway_transfer_fetcher.stop()
    busway_track_fetcher.stop()
    autocomplete_service.stop()


start()
