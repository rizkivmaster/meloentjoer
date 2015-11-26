from common import general_scheduler
from common.logging import logger_factory
from config import general_config
from fetcher.util import helper as __helper
from accessors.routes import train_route_accessor as __train_route_accessor

__logger = logger_factory.create_logger(__name__)


def __update():
    route_list = __helper.get_train_routes()
    for train_route in route_list:
        __train_route_accessor.upset_train_route(train_route)
    __logger.info('Updated')


__update_period = general_config.get_train_info_refresh_period()
__scheduler = general_scheduler.schedule(__update_period, __update)


def start():
    __update()
    __scheduler.start()
    __logger.info('Started')


def stop():
    __logger.info('Stopped')
    __scheduler.stop()
