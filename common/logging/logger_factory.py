import logging
import traceback
import sys




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
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - {0} - %(message)s'.format(name))
        ch.setFormatter(formatter)
        self.__logger.addHandler(ch)
        self.__logger.setLevel(logging.DEBUG)

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
