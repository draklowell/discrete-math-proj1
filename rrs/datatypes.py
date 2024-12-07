"""
Rapid Response Service library.
Module for datatypes.
"""

from collections import namedtuple

Map = namedtuple("Map", ("roads", "cities", "center"))
# roads: dict[str, Road], each key is a name of the road
# cities: dict[str, City], each key is a name of the city
# center: str, central city name

Road = namedtuple("Road", ("city1", "city2", "distance"))
# city1: str, city name
# city2: str, city name
# distance: float, distance of the road

City = namedtuple("City", ("roads",))
# roads: list[str], list of all road names connected to this city
# is_center: bool, True when city is central
