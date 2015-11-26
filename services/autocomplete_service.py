from accessors.routes import bus_route_accessor, train_route_accessor, walk_route_accessor, \
    busway_transfer_accessor
from common import general_scheduler
from common.logging import logger_factory
from common.util.TrieNode import TrieNode
from config import general_config

__logger = logger_factory.create_logger('autocomplete_service')
__trie = TrieNode()


def __update():
    try:
        bus_route_list = bus_route_accessor.get_all_bus_routes()
        word_pool = set()
        for route in bus_route_list:
            stations = route.stations
            for station in stations:
                word_pool.add(station)
        train_route_list = train_route_accessor.get_all_train_routes()
        """:type :list[TrainRoute]"""
        for route in train_route_list:
            for station in route.stations:
                word_pool.add(station)
        walk_route_list = walk_route_accessor.get_all_walk_routes()
        """:type :list[WalkRoute]"""
        for route in walk_route_list:
            word_pool.add(route.walk_from)
            word_pool.add(route.walk_to)
        busway_transfer_list = busway_transfer_accessor.get_all_busway_transfers()
        """:type :list[BuswayTransfer]"""
        for route in busway_transfer_list:
            word_pool.add(route.from_station)
            word_pool.add(route.to_station)
        for word in word_pool:
            add_keyword(word, word)
    except Exception, e:
        __logger.error(e)
    __logger.info('Updated')


__scheduler = general_scheduler.schedule(general_config.get_autocomplete_refresh_period(), __update)


def add_keyword(word, key):
    """
    :type word: str
    :type key: str
    :param word:
    :param key:
    :return:
    """
    __trie.add_word(word, key)


def get_words(key):
    """
    :type key:str
    :param key:
    :return:
    :rtype: list[str]
    """
    word_list = __trie.dfs(key)
    return list(word_list)


def start():
    __update()
    __scheduler.start()
    __logger.info('Started')


def stop():
    __scheduler.stop()
    __logger.info('Stopped')
