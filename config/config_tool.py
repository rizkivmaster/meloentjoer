import os
from common.databases.ModelBase import ModelBase
from sqlalchemy import Column, String

from common.databases.PostgreBase import PostgresAccessorBase
from common.logging import logger_factory
from prod_config import config as __prod_config
from local_config import config as __local_config


class ConfigRecord(ModelBase):
    __tablename__ = "ConfigTable"
    key = Column(String, primary_key=True)
    value = Column(String)

    def __init__(self, key, value):
        self.key = key
        self.value = value


database_url = os.environ['MELOENTJOER_DATABASE_URL']
__config_session = PostgresAccessorBase(ConfigRecord, database_url)
__logger = logger_factory.create_logger(__name__)


def get_integer(key):
    try:
        return int(get_string(key))
    except Exception, e:
        __logger.error(e.message)


def get_string(key):
    try:
        config_record = __config_session.query(ConfigRecord). \
            filter(ConfigRecord.key == key). \
            first()
        """ :type :ConfigRecord"""
        if config_record:
            return config_record.value
    except Exception, e:
        __logger.error(e.message)


def get_float(key):
    try:
        return float(get_string(key))
    except Exception, e:
        __logger.error(e)


def get_bool(key):
    try:
        return bool(get_integer(key))
    except Exception, e:
        __logger.error(e)


def set_integer(key, value):
    try:
        set_string(key, str(value))
    except Exception, e:
        __logger.error(e)


def set_bool(key, value):
    try:
        set_integer(key, 1 if value else 0)
    except Exception, e:
        __logger.error(e)


def set_string(key, value):
    try:
        config_record = __config_session.query(ConfigRecord).filter(ConfigRecord.key == key).first()
        if not config_record:
            __config_session.add(ConfigRecord(key, value))
        else:
            config_record.value = value
        __config_session.commit()
    except Exception, e:
        __logger.error(e)


def set_float(key, value):
    try:
        set_string(key, str(value))
    except Exception, e:
        __logger.error(e)


def deploy_local_configurations():
    __config_session.query(ConfigRecord).delete()
    __config_session.commit()
    for key, value in __local_config.iteritems():
        set_string(key, str(value))
    set_string('DATABASE_URL', database_url)


def deploy_production_configurations(remote_database_url):
    __config_session = PostgresAccessorBase(ConfigRecord, remote_database_url)
    __config_session.query(ConfigRecord).delete()
    __config_session.commit()
    for key, value in __prod_config.iteritems():
        set_string(key, str(value))
    set_string('DATABASE_URL', remote_database_url)
