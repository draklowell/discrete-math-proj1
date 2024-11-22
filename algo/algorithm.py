"""
Module for working with algorithms for graph
"""
from algo.datatypes import Map, Road

def get_components(map: Map, damaged_roads: dict[str, float]) -> list[list[Road]]:
    """
    Get isolated regions of the map.

    :param map: Map
    :param damaged_roads: dict[str, float], list of damaged roads

    :returns: list[list[Road]],
    """
    visited = set()
    components_mas = []
    # будемо починати з обл центра
    def dfs_iterative(start:str):
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
                    elif map.roads[r].city2 != node and map.roads[r].city2 not in visited:
                        stack.append(map.roads[r].city2)
        components_mas.append(temp)

    components = 0
    for city_name in map.cities:
        if city_name not in visited:
            components+=1
            dfs_iterative(city_name)
    return components_mas

def spanning_tree_prima(map: Map, nodes: list, damaged_roads: dict[str, float]) -> list[str]:
    """
    Building a spanning tree using the Prima algorithm
    """
    def find_nodes_with_same_roads():
        res = {}
        for road in damaged_roads:
            temp = []
            for ind,node in enumerate(nodes):
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
    while len(nodes) > 1:
        for road in nodes[0]:
            availvable_roads.append(road)

        availvable_roads = list(set(availvable_roads) - mst)

        choice = min(availvable_roads, key=lambda x: damaged_roads[x])

        to = set(map.roads[choice][:2])-visited
        from_ = visited & set(map.roads[choice][:2])

        for ind, r in enumerate(availvable_roads):
            if to in from_to[r] and len(from_to[r] & from_) >= 1:
                del availvable_roads[ind]
        nodes.pop(0)
        mst.add(choice)
    return mst
