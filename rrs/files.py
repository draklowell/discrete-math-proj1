"""
Rapid Response Service library.
Module for working with the map in the form of graph.
"""

from rrs.datatypes import Map, Road, City


def city_roads_names(city, file_listed) -> list:
    """
    Find all names of roads connected to the city.

    :param city: str, city name
    :param file_listed: list, list of file lines

    :returns: list[str], list of all road names connected to the city
    """
    return [line[: line.find(",")] for line in file_listed[1:] if city in line]


def read_map(path: str) -> Map:
    """
    Read map data from the file at the given path.

    :param path: str, path to the file

    :returns: Map
    """
    roads, cities = {}, {}

    with open(path, "r", encoding="utf-8") as file:
        listed_file = file.readlines()

        center_city = listed_file[0].strip()
        center_city_roads = city_roads_names(center_city, listed_file)
        cities.setdefault(center_city, City(roads=center_city_roads, is_center=True))

        for line in listed_file[1:]:
            road, c1, c2, distnce = line.split(", ")

            distnce = float(distnce.strip())
            roads.setdefault(road, Road(city1=c1, city2=c2, distance=distnce))

            c1_roads = city_roads_names(c1, listed_file)
            cities.setdefault(c1, City(c1_roads, is_center=False))
            c2_roads = city_roads_names(c2, listed_file)
            cities.setdefault(c2, City(c2_roads, is_center=False))

    return Map(roads, cities)


def read_damaged_roads(path: str) -> dict[str, float]:
    """
    Read list of damaged roads from the file at the given path.

    :param path: str, path to the file

    :returns: dict[str, float], damaged roads in the form of dict
    where key is the road name and value is the complexity of repairing
    it
    """
    damaged_roads = {}

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            road_name, damage = line.split(",")
            damaged_roads[road_name] = float(damage)

        return damaged_roads
