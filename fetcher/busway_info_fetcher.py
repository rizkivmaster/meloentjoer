from accessors.routes import bus_route_accessor as __bus_route_accessor
from common import general_scheduler as __general_scheduler
from config import general_config as __general_config
from fetcher.util import helper as __helper
from common.logging import logger_factory

__logger = logger_factory.create_logger(__name__)


def __update():
    route_list = __helper.get_busway_routes()
    for route in route_list:
        __bus_route_accessor.upset_bus_route(route)
    __logger.info('Updated')


__update_period = __general_config.get_geo_refresh_period()
__scheduler = __general_scheduler.schedule(__update_period, __update)


def start():
    # hack: force to update immediately
    __update()
    __scheduler.start()
    __logger.info('Started')


def stop():
    __logger.info('Stopped')
    __scheduler.stop()
