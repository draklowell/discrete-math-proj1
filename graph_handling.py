"""
Module for working with the map in the form of graph.
"""

from collections import namedtuple

Map = namedtuple("Map", ("roads", "cities"))
# roads: dict[str, Road], each key is a name of the road
# cities: dict[str, City], each key is a name of the city

Road = namedtuple("Road", ("city1", "city2", "distance"))
# city1: str, city name
# city2: str, city name
# distance: float, distance of the road

City = namedtuple("City", ("roads", "is_center"))
# roads: list[str], list of all road names connected to this city
# is_center: bool, True when city is central


def read_map(path: str) -> Map:
    """
    Read map data from the file at the given path.

    :param path: str, path to the file

    :returns: Map
    """
    # with open(path, 'r', encoding='utf-8') as f:


def read_damaged_roads(path: str) -> dict[str, float]:
    """
    Read list of damaged roads from the file at the given path.

    :param path: str, path to the file

    :returns: dict[str, float], damaged roads in the form of dict
    where key is the road name and value is the complexity of repairing
    it
    """
    damaged_roads = {}

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            road_name, damage = line.split(',')
            damaged_roads[road_name] = float(damage)

        return damaged_roads


def get_components(map: Map, damaged_roads: dict[str, float]) -> list[set[str]]:
    """
    Get isolated regions of the map.

    :param map: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: list[set[str]], list of all isolated regions, where each region
    is represented by the set of cities in it
    """
    ...
