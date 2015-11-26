from accessors.entity.WalkRoute import WalkRoute
from common.databases.ModelBase import ModelBase
from common.databases.PostgreBase import PostgresAccessorBase
from config import general_config as __config
from sqlalchemy import String, Column
from common.logging import logger_factory

__logger = logger_factory.create_logger(__name__)


def index(walk_route):
    """
    :type walk_route WalkRoute
    :param walk_route:
    :return:
    """
    return walk_route.walk_from + '_' + walk_route.walk_to


class WalkRouteModel(ModelBase):
    __tablename__ = "WalkRouteModel"
    index = Column(String, primary_key=True)
    walk_from = Column(String)
    walk_to = Column(String)

    def __init__(self):
        self.index = None
        self.walk_from = None
        self.walk_to = None

    def to_walk_route(self):
        walk_route = WalkRoute()
        walk_route.walk_from = self.walk_from
        walk_route.walk_to = self.walk_to
        return walk_route

    def from_walk_route(self, walk_route):
        self.index = index(walk_route)
        self.walk_to = walk_route.walk_to
        self.walk_from = walk_route.walk_from


walk_routes_session = PostgresAccessorBase(WalkRouteModel,
                                           __config.get_database_url())


def reset():
    walk_routes_session.query(WalkRouteModel).delete()
    walk_routes_session.commit()


def get_walk_route(walk_route):
    """
    :rtype WalkRoute
    :type walk_route:WalkRoute
    :rtype :WalkRoute
    """
    raw_walk_route = walk_routes_session.query(WalkRouteModel).filter(
        WalkRouteModel.index == index(walk_route)).first()
    return raw_walk_route.to_walk_route() if raw_walk_route is not None else None


def get_all_walk_routes():
    """
    :return:
    :rtype dict[str,WalkRoute]
    """
    raw_walk_route_list = walk_routes_session.query(WalkRouteModel).all()
    walk_route_list = [walk_route.to_walk_route() for walk_route in raw_walk_route_list]
    return walk_route_list


def upset_walk_route(walk_route):
    """
    :type walk_route: WalkRoute
    :param walk_route:
    :return:
    """
    raw_walk_route = get_walk_route(walk_route)
    if raw_walk_route is None:
        raw_walk_route = WalkRouteModel()
        raw_walk_route.from_walk_route(walk_route)
        walk_routes_session.add(raw_walk_route)
    walk_routes_session.commit()
