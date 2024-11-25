"""
Rapid Response Service library.
Module for working with algorithms for graph.
"""

from rrs.datatypes import Map, Road, City


def get_isolated_roads(map: Map, damaged_roads: dict[str, float]) -> list[list[str]]:
    """
    Get isolated regions of the map.

    :param map: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: list[list[str]], roads names that connect isolated parts to other parts of the map
    """
    visited = set()
    components_mas = []

    # будемо починати з обл центра
    def dfs_iterative(start: str):
        stack = [start]  # Ініціалізуємо стек із початковим вузлом
        temp = []
        while stack:
            node = stack.pop()

            if node not in visited:
                visited.add(node)

                for r in map.cities[node].roads:
                    if r in damaged_roads:
                        temp.append(r)

                # Додаємо сусідів вузла у стек (у зворотному порядку, щоб порядок обходу був правильний)
                for r in map.cities[node].roads:
                    if r in damaged_roads:
                        continue
                    if map.roads[r].city1 != node and map.roads[r].city1 not in visited:
                        stack.append(map.roads[r].city1)
                    elif (
                        map.roads[r].city2 != node and map.roads[r].city2 not in visited
                    ):
                        stack.append(map.roads[r].city2)
        components_mas.append(temp)

    components = 0
    for city_name in map.cities:
        if city_name not in visited:
            components += 1
            dfs_iterative(city_name)
    return components_mas


def get_roads_to_recover(
    map: Map, isolated_roads: list[list[str]], damaged_roads: dict[str, float]
) -> list[str]:
    """
    Get roads to recover as a spanning tree using the Prima algorithm.

    :param map: Map
    :param isolated_roads: list[list[str]], roads names that connect isolated regions from
    get_isolated_roads
    :param damaged_roads: dict[str, float], list of damaged roads
    """

    def find_nodes_with_same_roads():
        res = {}
        for road in damaged_roads:
            temp = []
            for ind, node in enumerate(isolated_roads):
                if road in node:
                    temp.append(ind)
                if len(temp) == 2:
                    res[road] = temp
                    break
        return res

    mst = set()  # Список для збереження мінімального кістякового дерева
    visited = set()  # Множина для збереження відвіданих вузлів
    from_to = find_nodes_with_same_roads()

    availvable_roads = []
    while len(isolated_roads) > 1:
        for road in isolated_roads[0]:
            availvable_roads.append(road)

        availvable_roads = list(set(availvable_roads) - mst)

        choice = min(availvable_roads, key=lambda x: damaged_roads[x])

        to = set(map.roads[choice][:2]) - visited
        from_ = visited & set(map.roads[choice][:2])

        for ind, r in enumerate(availvable_roads):
            if to in from_to[r] and len(from_to[r] & from_) >= 1:
                del availvable_roads[ind]
        isolated_roads.pop(0)
        mst.add(choice)

    return mst
