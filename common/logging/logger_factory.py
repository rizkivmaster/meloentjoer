import logging
import traceback
import sys


#
# logging.basicConfig(
#     filename='mj.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - {0} - %(message)s'.format(name))


class Logger(object):
    def __init__(self, name=None):
        """
        :type name: str
        :param name:
        :return:
        """
        self.__logger = logging.getLogger(name)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - {0} - %(message)s'.format(name))
        ch.setFormatter(formatter)
        self.__logger.addHandler(ch)

    def error(self, e):
        """
        :type e :Exception
        :param e:
        :return:
        """
        self.__logger.exception(e)

    def info(self, message):
        self.__logger.info(message)

    def debug(self, message):
        self.__logger.debug(message)


def create_logger(name):
    return Logger(name)
