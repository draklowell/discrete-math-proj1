"""
Module for working with the map in the form of graph.
"""

from algo.datatypes import Map


def read_map(path: str) -> Map:
    """
    Read map data from the file at the given path.

    :param path: str, path to the file

    :returns: Map
    """
    pass


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
