"""
Rapid Response Service library.
Module for working with algorithms for graph.
"""

from rrs.datatypes import Map, Road, City


def check_same_road(map: Map, check_road: str) -> bool:
    """
    Checks whether there is another road connecting the same two cities as the given road.

    :param map: Map
        A data structure representing the map, containing roads and cities.
        - roads: A dictionary where each key is a road name (str) and the value is a Road object.
        - cities: A dictionary where each key is a city name (str) and the value is a City object.
    :param check_road: str
        The name of the road to check for redundancy.

    :return: bool
        Returns True if there is another road connecting the same two cities as the given road.
        Returns False otherwise.
    """
    city1, city2 = map.roads[check_road].city1, map.roads[check_road].city2
    for road_in_city in map.cities[city1].roads:
        if road_in_city != check_road and road_in_city in map.cities[city2].roads:
            return True
    return False


def get_isolated_roads(
    map: Map, damaged_roads: dict[str, float]
) -> list[tuple[list[Road], list[City]]]:
    """
    Get isolated regions of the map.

    :param map: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: list[tuple[list[Road],list[City]]], roads names that connect
    isolated parts to other parts of the map and city names in this connectivity component
    """
    visited_cities = set()
    isolated_roads = []

    # Будемо починати з обл центра
    def dfs_iterative(start: str):
        stack = [start]  # Ініціалізуємо стек із початковим вузлом
        region_roads = []
        region_cities = []
        while stack:
            city = stack.pop()

            if city not in visited_cities:
                visited_cities.add(city)
                region_cities.append(city)

            for road in map.cities[city].roads:
                if road in damaged_roads and road not in region_roads:
                    if not check_same_road(map, road):
                        region_roads.append(road)

            for road in map.cities[city].roads:
                if road in damaged_roads:
                    continue

                city1 = map.roads[road].city1
                city2 = map.roads[road].city2

                if city1 != city and city1 not in visited_cities:
                    stack.append(city1)
                elif city2 != city and city2 not in visited_cities:
                    stack.append(city2)

        isolated_roads.append((region_roads, region_cities))

    for city_name in map.cities:
        if city_name not in visited_cities:
            dfs_iterative(city_name)
    return isolated_roads


def get_roads_to_recover(
    map: Map,
    isolated_roads_city: list[tuple[list[Road], list[City]]],
    damaged_roads: dict[str, float],
) -> set[str]:
    """
    Get roads to recover as a spanning tree using the Prima algorithm.

    :param map: Map
    :param isolated_roads_city: list[tuple[list[Road],list[City]]],
    roads names that connect isolated regions
    and city names in this connectivity component from get_isolated_roads
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: set[str], roads to recover

    """

    def find_nodes_with_same_roads():
        res = {}
        for road in damaged_roads:
            components_connected = []
            for index, component in enumerate(isolated_roads_city):
                component = component[0]
                if road in component:
                    components_connected.append(index)
                if len(components_connected) == 2:
                    res[road] = components_connected
                    break
        return res

    mst = set()  # Список для збереження мінімального кістякового дерева
    visited = set()  # Множина для збереження відвіданих вузлів
    from_to = find_nodes_with_same_roads()

    availvable_roads = []
    while len(isolated_roads_city) > 1:
        availvable_roads.extend(isolated_roads_city[0][0])

        availvable_roads = list(set(availvable_roads) - mst)

        choice = min(availvable_roads, key=lambda x: damaged_roads[x])

        to = set(map.roads[choice][:2]) - visited
        from_ = visited & set(map.roads[choice][:2])

        for index, road in enumerate(availvable_roads):
            if to in from_to[road] and len(from_to[road] & from_) >= 1:
                del availvable_roads[index]
                for isolated_road_index, component in enumerate(isolated_roads_city):
                    component = component[0]
                    if road in component:
                        component[isolated_road_index].remove(road)
        isolated_roads_city.pop(0)
        mst.add(choice)
    return mst
