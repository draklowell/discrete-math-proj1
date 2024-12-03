"""
Rapid Response Service library.
Module for working with algorithms for graph.
"""

from rrs.datatypes import Map, Road, City

def add_roads_to_componenets(map: Map, damaged_roads: dict[str, float], city_components: list[list[list[Road],list[City]]]) -> list[list[list[Road],list[City]], dict[list[int]]]:
    """
    """
    road_with_component = {}
    for road in damaged_roads:
        city1 = map.roads[road].city1
        city2 = map.roads[road].city2
        for index,component in enumerate(city_components):
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

    city_components.append(road_with_component)
    return city_components



def get_isolated_roads(map: Map, damaged_roads: dict[str, float]) -> list[list[list[Road],list[City]], dict[list]]:
    """
    Get isolated regions of the map.

    :param map: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: list[tuple[list[Road],list[City]]], roads names that connect
    isolated parts to other parts of the map and city names in this connectivity component 
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

            for road in map.cities[city].roads:
                if road in damaged_roads:
                    continue

                city1 = map.roads[road].city1
                city2 = map.roads[road].city2

                if city1 != city and city1 not in visited_cities:
                    stack.append(city1)
                elif city2 != city and city2 not in visited_cities:
                    stack.append(city2)

        isolated_roads.append([region_roads,region_cities])

    # Будемо починати з обл центра
    dfs_iterative(map.center)
    for city_name in map.cities:
        if city_name not in visited_cities:
            dfs_iterative(city_name)

    return add_roads_to_componenets(map,damaged_roads,isolated_roads)


def get_roads_to_recover(
    map: Map,
    isolated_regions: list,
    damaged_roads: dict[str, float],
) -> set[str]:
    """
    Get roads to recover as a spanning tree using the Prima algorithm.

    :param map: Map
    :param isolated_regions: list,
        road names that connect isolated regions
        and city names in this connectivity component from get_isolated_roads
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: set[str], roads to recover
    """

    components = list(zip(*isolated_regions[0]))[0]
    roads = isolated_regions[1]

    roads_to_recover = set()
    visited_components = set()

    available_roads = set(components[0])
    while available_roads:
        road = min(available_roads, key=lambda x: damaged_roads[x]*map.roads[x].distance)
        available_roads.remove(road)

        if roads[road][0] not in visited_components:
            available_roads |= set(components[roads[road][0]])
            visited_components.add(roads[road][0])
            roads_to_recover.add(road)

        if roads[road][1] not in visited_components:
            available_roads |= set(components[roads[road][1]])
            visited_components.add(roads[road][1])
            roads_to_recover.add(road)

    return roads_to_recover
