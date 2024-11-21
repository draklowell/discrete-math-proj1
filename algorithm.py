"""
Module for working with algorithms for graph
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

if __name__ == '__main__':
    # import doctest
    # print(doctest.testmod())
    map = Map({'r1':Road('c1', 'c2', 4), 'r2':Road('c2', 'c3', 2), 'r3':Road('c2', 'c4', 5)}, {'c1': City(['r1'], True), 'c2': City(['r1','r2', 'r3'], False), 'c3': City(['r2'], False), 'c4': City(['r3'], False)})
    damaged_roads = {'r2': 2.0, 'r3': 5.0}
    print(get_components(map,damaged_roads))
    print(spanning_tree_prima(map,[['r2', 'r3'], ['r2'], ['r3']],damaged_roads))
