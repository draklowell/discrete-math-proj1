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
    ...


def read_damaged_roads(path: str) -> dict[str, float]:
    """
    Read list of damaged roadsfrom the file at the given path.

    :param path: str, path to the file

    :returns: dict[str, float], damaged roads in the form of dict
    where key is the road name and value is the complexity of repairing
    it
    """
    ...


def get_components(map: Map, damaged_roads: dict[str, float]) -> list[set[str]]:
    """
    Get isolated regions of the map.

    :param map: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: list[set[str]], list of all isolated regions, where each region
    is represented by the set of cities in it
    """
    roads, cities = map

    all_cities_graph = {}
    for el in cities.keys():
        all_cities_graph.setdefault(el, [])

    for road, value in roads.items():
        if road not in damaged_roads.keys():
            all_cities_graph[value.city1].append(value.city2)
            all_cities_graph[value.city2].append(value.city1)

    regions = []
    def find_connected_cities(city):
        region.add(city)
        visited_cities.add(city)
        for new_city in all_cities_graph.get(city):
            if not new_city in visited_cities and not new_city in region:
                find_connected_cities(new_city)
        return region

    visited_cities = set()
    for city in all_cities_graph.keys():
        region = set()
        if city not in visited_cities:
            regions.append(find_connected_cities(city))

    return regions
