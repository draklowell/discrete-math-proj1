"""
Rapid Response Service library.
Module for working with algorithms for graph.
"""

from rrs.datatypes import City, Map, Road


def add_roads_to_componenets(
    map_: Map,
    damaged_roads: dict[str, float],
    city_components: list[list[list[Road], list[City]]],
) -> tuple[list[list[str]], dict[list[int]]]:
    """
    Add roads connecting different components to the isolated roads list.

    :param map_: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: tuple[list[list[str]], dict[list[int]]],
        1. The first list contains components as the list in the
           [roads, cities] form, where roads and cities are lists of
           names of roads and cities respectively;
        2. The second dict contains damaged roads as the dict, where
           keys are road names and values are lists of component indecies,
           that are connected with this road.
    """
    road_with_component = {}
    for road in damaged_roads:
        city1 = map_.roads[road].city1
        city2 = map_.roads[road].city2
        for index, component in enumerate(city_components):
            component = component[1]
            if city1 in component and city2 in component:
                break
            if city1 in component:
                city_components[index][0].append(road)
                if road in road_with_component:
                    road_with_component[road].append(index)
                else:
                    road_with_component[road] = [index]
            if city2 in component:
                city_components[index][0].append(road)
                if road in road_with_component:
                    road_with_component[road].append(index)
                else:
                    road_with_component[road] = [index]

    return city_components, road_with_component


def get_isolated_regions(
    map_: Map, damaged_roads: dict[str, float]
) -> tuple[list[list[str]], dict[list[int]]]:
    """
    Get isolated regions of the map.

    :param map_: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: tuple[list[list[str]], dict[list[int]]],
        1. The first list contains components as the list in the
           [roads, cities] form, where roads and cities are lists of
           names of roads and cities respectively;
        2. The second dict contains damaged roads as the dict, where
           keys are road names and values are lists of component indecies,
           that are connected with this road.
    """
    visited_cities = set()
    isolated_roads = []

    def dfs_iterative(start: str):
        stack = [start]
        region_roads = []
        region_cities = []
        while stack:
            city = stack.pop()

            if city not in visited_cities:
                visited_cities.add(city)
                region_cities.append(city)

            for road in map_.cities[city].roads:
                if road in damaged_roads:
                    continue

                city1 = map_.roads[road].city1
                city2 = map_.roads[road].city2

                if city1 != city and city1 not in visited_cities:
                    stack.append(city1)
                elif city2 != city and city2 not in visited_cities:
                    stack.append(city2)

        isolated_roads.append([region_roads, region_cities])

    # Будемо починати з обл центра
    dfs_iterative(map_.center)
    for city_name in map_.cities:
        if city_name not in visited_cities:
            dfs_iterative(city_name)

    return add_roads_to_componenets(map_, damaged_roads, isolated_roads)


def get_roads_to_recover(
    map_: Map,
    isolated_regions: tuple[list[list[str]], dict[list[int]]],
    damaged_roads: dict[str, float],
) -> set[str]:
    """
    Get roads to recover as a spanning tree using the Prima algorithm.

    :param map_: Map
    :param isolated_regions: tuple[list[list[str]], dict[list[int]]],
        isolated regions from the get_isolated_regions function
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: set[str], roads to recover
    """
    components, roads = isolated_regions

    roads_to_recover = set()
    visited_components = set()

    available_roads = set(components[0][0])
    while available_roads:
        road = min(
            available_roads, key=lambda x: damaged_roads[x] * map_.roads[x].distance
        )
        available_roads.remove(road)

        if roads[road][0] not in visited_components:
            available_roads |= set(components[roads[road][0]][0])
            visited_components.add(roads[road][0])
            roads_to_recover.add(road)

        if roads[road][1] not in visited_components:
            available_roads |= set(components[roads[road][1]][0])
            visited_components.add(roads[road][1])
            roads_to_recover.add(road)

    return roads_to_recover
