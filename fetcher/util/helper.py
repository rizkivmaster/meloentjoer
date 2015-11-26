from accessors.entity.BusRoute import BusRoute
from accessors.entity.BuswayTransfer import BuswayTransfer
from accessors.entity.TrainRoute import TrainRoute
from accessors.entity.WalkRoute import WalkRoute
from fetcher.entity.BusTrackData import BusTrackData

__author__ = 'traveloka'

from common.logging import logger_factory
import urllib2
import xml.etree.ElementTree as Et

from bs4 import BeautifulSoup
from common.util.LinkedHash import LinkedHash
import re

__logger = logger_factory.create_logger('helper')


def scrap(link):
    """
    :type link: str
    :param link: string
    :return:
    """
    html = urllib2.urlopen(link)
    scrapper = BeautifulSoup(html, 'html.parser')
    return scrapper


def row_parser(text):
    innertext = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]', text)
    if not len(innertext) == 0:
        return re.sub('[^a-zA-Z0-9 ]+', '', innertext[0]).strip()
    else:
        return ''


def multi_row_parser(text):
    text_lines = text.split('\n')
    return_line = []
    for line in text_lines:
        inner_text = re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]', line)
        if not len(inner_text) == 0:
            return_line.append(re.sub('[^a-zA-Z0-9 ]+', '', inner_text[0]))
        else:
            return ''
    return ','.join(return_line)


def multi_href_parser(element):
    buffers = []
    return_lists = set()
    return_maps = dict()
    items = element.find_all('a')
    for item in items:
        if item.name == 'a':
            if item.has_attr('class') and item['class'][0] == 'image':
                buffers.append(item['title'])
            else:
                for a_buffer in buffers:
                    return_lists.add(a_buffer + '_' + str(item.getText()))
                    return_maps[a_buffer + '_' + str(item.getText())] = (a_buffer, str(item.getText()))
                buffers = []
        if item.next_sibling is not None:
            if item.next_sibling.string is not None:
                if not item.next_sibling.strip() == '':
                    for a_buffer in buffers:
                        return_lists.add(a_buffer + '_' + str(item.next_sibling).strip())
                        value = (a_buffer, str(item.next_sibling).strip())
                        return_maps[a_buffer + '_' + str(item.next_sibling).strip()] = value

                    buffers = []
    return return_lists, return_maps


def get_busway_routes(callback=None):
    """
    scrape the routes
    :type callback:common.callbacks.Callback


    :rtype list[BusRoute]
    """
    routes_list = []
    try:
        scrapper = scrap("https://en.wikipedia.org/wiki/TransJakarta_Corridors")
        main_content = scrapper.find('div', attrs={'id': 'mw-content-text'})
        tables = main_content.find_all('table', {'class': 'wikitable'})
        for table in tables:
            route = BusRoute()
            rows = table.find_all('tr')
            corridor_name = rows[0].find('th').find('a')['title']
            new_rows = rows[2:]
            station_list = []
            for row in new_rows:
                station_name = row_parser(row.find_all('td')[1].getText())
                station_list.append("Halte " + station_name)
            route.stations = station_list
            route.corridor_name = corridor_name
            routes_list.append(route)
    except Exception, e:
        callback.on_failure(e)
        __logger.error(e)
    return routes_list


def get_train_routes():
    """
    :rtype :list[TrainRoute]
    :return:
    """
    train_routes_list = []
    train_scrapper = scrap(
        'https://en.wikipedia.org/w/index.php?title=KA_Commuter_Jabodetabek&oldid=683328854')
    raw_tables = train_scrapper.select('dl > dd > b')
    for table in raw_tables:
        line_name = \
            re.findall('[a-zA-Z0-9 ]+[a-zA-Z0-9]', table.parent.parent.previousSibling.previousSibling.string)[
                0].strip()
        station_list = LinkedHash(
            map(lambda x: 'Stasiun ' + x.strip(),
                re.sub(u'\u2192', ',', re.sub('\\.', '', table.parent.getText())).split(',')))
        train_route = TrainRoute()
        train_route.line_name = line_name
        train_route.stations = station_list
        train_routes_list.append(train_route)
    return train_routes_list


def get_walk_routes():
    """
    :rtype :list[WalkRoute]
    :return:
    """
    walk_routes_list = []
    try:
        scrapper = scrap("https://en.wikipedia.org/wiki/TransJakarta_Corridors")
        main_content = scrapper.find('div', attrs={'id': 'mw-content-text'})
        tables = main_content.find_all('table', {'class': 'wikitable'})
        for table in tables:
            rows = table.find_all('tr')
            new_rows = rows[2:]
            for row in new_rows:
                busway_station = row_parser(row.find_all('td')[1].getText())
                nearby_segments = row.find_all('td')
                if len(nearby_segments) > 3:
                    nearby_segment = nearby_segments[3]
                    nearby_set, nearby_map = multi_href_parser(nearby_segment)
                    for key in nearby_set:
                        cleaned_nearby = re.sub('Bus Terminal', '', nearby_map[key][1])
                        cleaned_nearby = re.sub('Station', '', cleaned_nearby)
                        cleaned_nearby = cleaned_nearby.strip()
                        walk_route = WalkRoute()
                        walk_route.walk_from = 'Halte ' + busway_station
                        if nearby_map[key][0] == 'Bus Terminal':
                            walk_route.walk_to = 'Terminal ' + cleaned_nearby
                            walk_routes_list.append(walk_route)
                        if nearby_map[key][0] == 'Train Station':
                            walk_route.walk_to = 'Stasiun ' + cleaned_nearby
                            walk_routes_list.append(walk_route)

    except Exception, e:
        __logger.error(e)
    finally:
        return walk_routes_list


def get_busway_transfers():
    """
    :rtype :list[BuswayTransfer]
    :return:
    """
    busway_transfers_list = []
    try:
        scrapper = scrap("https://en.wikipedia.org/wiki/TransJakarta_Corridors")
        main_content = scrapper.find('div', attrs={'id': 'mw-content-text'})
        tables = main_content.find_all('table', {'class': 'wikitable'})
        filter_set = set()
        for table in tables:
            rows = table.find_all('tr')
            transfer_rows = rows[2:]
            for row in transfer_rows:
                from_busway_station = row_parser(row.find_all('td')[1].getText())
                transfer_set, transfer_map = multi_href_parser(row.find_all('td')[2])
                for transfer_key in transfer_set:
                    to_busway_station = transfer_map[transfer_key][1]
                    # no need to state a transfer between stations with similar name
                    if not from_busway_station == to_busway_station:
                        halt_list = list()
                        halt_list.append(from_busway_station)
                        halt_list.append(to_busway_station)
                        halt_list.sort()
                        filter_set.add((halt_list[0], halt_list[1]))
        for halt_pair in filter_set:
            busway_transfer = BuswayTransfer()
            busway_transfer.from_station = 'Halte ' + halt_pair[0]
            busway_transfer.to_station = 'Halte ' + halt_pair[1]
            busway_transfers_list.append(busway_transfer)
    except Exception, e:
        __logger.error(e)
    finally:
        return busway_transfers_list


def get_session_key():
    req = urllib2.Request('http://smartcityjakarta.com/bustrack/')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    req.add_header('Cache-Control', 'max-age=0')
    req.add_header('Connection', 'keep-alive')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
    req.add_header('Host', 'smartcityjakarta.com')
    test = urllib2.urlopen(req)
    try:
        for value in test.info().values():
            if 'PHPSESSID' in value:
                return value.split(";")[0]
    except Exception, e:
        __logger.error(e)
    return None


def request_buses():
    """
    :rtype dict[str,BusTrackData]
    :return:
    """
    req = urllib2.Request('http://smartcityjakarta.com/bustrack/stadtbus_rapperswil.php')
    req.add_header('Accept', 'application/xml, text/xml, */*; q=0.01')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Connection', 'keep-alive')
    req.add_header('Accept-Language', 'en-US,en;q=0.5')
    req.add_header('Cache-Control', 'max-age=0')
    req.add_header('Connection', 'keep-alive')
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0')
    req.add_header('Host', 'smartcityjakarta.com')
    req.add_header('Referer', 'http://smartcityjakarta.com/bustrack/')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    session_key = get_session_key()
    if session_key is None:
        __logger.error(Exception('Cannot get session key'))
        return None
    req.add_header('Cookie', session_key)
    response = urllib2.urlopen(req)
    htmlfile = response.read()
    root = Et.fromstring(htmlfile)
    dix = dict()
    for bus in root[3]:
        dixx = dict()
        for node in bus:
            dixx[node.tag] = node.text
        bus_track_data = BusTrackData()
        bus_track_data.name = dixx['identifier']
        bus_track_data.longitude = float(dixx['lon'])
        bus_track_data.latitude = float(dixx['lat'])
        bus_track_data.speed = float(dixx['speedKmh'])
        dix[bus_track_data.name] = bus_track_data
    return dix
