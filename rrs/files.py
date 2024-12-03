"""
Rapid Response Service library.
Module for working with the map in the form of graph.
"""

from rrs.datatypes import Map, Road, City


def write_dot_graph(path: str, map_: Map, damaged_roads: dict[str, float]) -> str:
    """
    Generate .dot graph from the graph data.

    :param path: str, path to the .dot file
    :param map_: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: str, .dot graph
    """
    with open(path, "w", encoding="utf8") as file:
        file.write("graph{\n")
        for road_name, road in map_.roads.items():
            if road_name in damaged_roads:
                file.write(f'"{road.city1}" -- "{road.city2}" ')
                file.write(
                    f'[weight={road.distance}; label="{road_name}({damaged_roads[road_name]})"'
                )
                file.write(";color=red]\n")
            else:
                file.write(f'"{road.city1}" -- "{road.city2}"')
                file.write(f'[weight={road.distance}; label="{road_name}"]\n')
        file.write("}\n")


def get_city_roads_names(city: str, listed_file: list[str]) -> list[str]:
    """
    Find all names of roads connected to the city.

    :param city: str, city name
    :param listed_file: list[str], list of file lines

    :returns: list[str], list of all road names connected to the city
    """
    return [line[: line.find(",")] for line in listed_file[1:] if city in line]


def read_map(path: str) -> Map:
    """
    Read map data from the file at the given path.

    :param path: str, path to the file

    :returns: Map
    """
    roads, cities = {}, {}

    with open(path, "r", encoding="utf-8") as file:
        listed_file = file.readlines()

        center = listed_file[0].strip()

        for line in listed_file[1:]:
            road, city1, city2, distance = line.split(", ")

            city1 = city1.strip()
            city2 = city2.strip()
            distance = float(distance.strip())
            roads.setdefault(road, Road(city1=city1, city2=city2, distance=distance))

            city1_roads = get_city_roads_names(city1, listed_file)
            cities.setdefault(city1, City(city1_roads))
            city2_roads = get_city_roads_names(city2, listed_file)
            cities.setdefault(city2, City(city2_roads))

    return Map(roads, cities, center)


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
            damaged_roads[road_name.strip()] = float(damage.strip())

        return damaged_roads
