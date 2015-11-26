import config_tool


def get_database_url():
    """
    :rtype
    :return:
    """
    return config_tool.get_string('DATABASE_URL')


def get_host_url():
    return config_tool.get_string('HOST_URL')


def get_mapping_threshold():
    return config_tool.get_float("mapping_threshold")


def get_geo_refresh_period():
    return config_tool.get_integer("geo_refresh_period")


def get_busway_transfer_refresh_period():
    return config_tool.get_integer("busway_transfer_refresh_period")


def get_train_info_refresh_period():
    return 10


def get_walk_route_refresh_period():
    return 10


def get_autocomplete_refresh_period():
    """
    :rtype int
    :return:
    """
    return 2


def get_default_eta():
    """
    :rtype int
    :return:
    """
    return 60


def get_default_price():
    """
    :rtype int
    :return:
    """
    return 0


def get_thread_size():
    """
    :rtype int
    :return:
    """
    return 32


def get_eta_refresh_period():
    """
    :rtype int
    :return:
    """
    return 2
