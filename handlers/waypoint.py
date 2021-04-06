import os
from collections import OrderedDict

import xmltodict
from constant import *


def load_waypoint():
    if not os.path.exists(HELIOS_WAYPOINT_FILE):
        return []
    with open(f'{HELIOS_WAYPOINT_FILE}') as fd:
        waypoint = xmltodict.parse(fd.read())
    return waypoint


def get_waypoints():
    waypoint = load_waypoint()
    if not waypoint:
        return waypoint
    return parse_waypoint(waypoint)


def parse_waypoint(waypoint):
    try:
        coords = waypoint['kml']['Document']['Placemark']['LineString']['coordinates']
        coords = coords.split(" ")
        return list(map(lambda x: x.split(','), coords))
    except KeyError:
        return []
