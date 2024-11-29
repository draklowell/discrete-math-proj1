"""
Rapid Response Service library.
Module for working with algorithms for graph.
"""

from rrs.datatypes import Map


def get_isolated_roads(map_: Map, damaged_roads: dict[str, float]) -> list[set[str]]:
    """
    Get isolated regions of the map.

    :param map: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: list[set[str]], roads names that connect isolated parts to other parts of the map
    """
    visited_cities = set()
    isolated_roads = []

    # Будемо починати з обл центра
    def dfs_iterative(start: str):
        stack = [start]  # Ініціалізуємо стек із початковим вузлом
        region_roads = set()
        while stack:
            city = stack.pop()

            if city in visited_cities:
                continue

            visited_cities.add(city)
            for road in map_.cities[city].roads:
                if road in damaged_roads:
                    region_roads.add(road)

                # Додаємо сусідів вузла у стек (у зворотному порядку, щоб порядок
                # обходу був правильний)
                for road in map_.cities[city].roads:
                    if road in damaged_roads:
                        continue

                    city1 = map_.roads[road].city1
                    city2 = map_.roads[road].city2

                    if city1 != city and city1 not in visited_cities:
                        stack.append(city1)
                    elif city2 != city and city2 not in visited_cities:
                        stack.append(city2)

        isolated_roads.append(region_roads)

    for city_name in map_.cities:
        if city_name not in visited_cities:
            dfs_iterative(city_name)
    return isolated_roads


def get_roads_to_recover(
    map_: Map, isolated_roads: list[list[str]], damaged_roads: dict[str, float]
) -> set[str]:
    """
    Get roads to recover as a spanning tree using the Prima algorithm.

    :param map: Map
    :param isolated_roads: list[list[str]], roads names that connect isolated regions from
    get_isolated_roads
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: set[str], roads to recover
    """

    from_to = {}
    for road in damaged_roads:
        components_connected = []
        for index, component in enumerate(isolated_roads):
            if road in component:
                components_connected.append(index)

            if len(components_connected) == 2:
                from_to[road] = tuple(components_connected)
                break

    mst = set()  # Список для збереження мінімального кістякового дерева
    visited = set()  # Множина для збереження відвіданих вузлів

    available_roads = []
    while len(isolated_roads) > 1:
        available_roads.extend(isolated_roads[0])
        available_roads = list(set(available_roads) - mst)

        choice = min(available_roads, key=lambda x: damaged_roads[x])

        to = set(map_.roads[choice][:2]) - visited
        from_ = visited & set(map_.roads[choice][:2])

        for index, road in enumerate(available_roads):
            if to in from_to[road] and len(from_to[road] & from_) >= 1:
                del available_roads[index]
                for isolated_road_index, component in enumerate(isolated_roads):
                    if road in component:
                        component[isolated_road_index].remove(road)
        isolated_roads.pop(0)
        mst.add(choice)

    return mst
