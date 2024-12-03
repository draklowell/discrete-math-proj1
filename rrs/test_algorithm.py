from rrs.algorithm import (
    add_roads_to_componenets,
    get_isolated_regions,
    get_roads_to_recover,
)
from rrs.files import read_damaged_roads, read_map


def test_add_roads_to_components():
    map_ = read_map("examples/small-map.csv")
    damaged_roads = read_damaged_roads("examples/small-damaged-roads.csv")
    isolated_regions = [
        [[], ["Deannamouth", "New Shannon"]],
        [[], ["Port Jonathan", "North Sydneyview"]],
        [[], ["Omarfurt"]],
        [[], ["Lawrenceland", "Meadowsberg"]],
    ]
    assert add_roads_to_componenets(map_, damaged_roads, isolated_regions) == (
        [
            [["E7", "M8", "T13", "M14"], ["Deannamouth", "New Shannon"]],
            [["T2", "M8", "H10", "M11", "T13"], ["Port Jonathan", "North Sydneyview"]],
            [["T2", "E7", "M9", "T12", "M14"], ["Omarfurt"]],
            [["M9", "H10", "M11", "T12"], ["Lawrenceland", "Meadowsberg"]],
        ],
        {
            "T2": [1, 2],
            "E7": [0, 2],
            "M8": [0, 1],
            "M9": [2, 3],
            "H10": [1, 3],
            "M11": [1, 3],
            "T12": [2, 3],
            "T13": [0, 1],
            "M14": [0, 2],
        },
    )


def test_get_isolated_regions():
    map_ = read_map("examples/small-map.csv")
    damaged_roads = read_damaged_roads("examples/small-damaged-roads.csv")
    assert get_isolated_regions(map_, damaged_roads) == (
        [
            [["E7", "M8", "T13", "M14"], ["Deannamouth", "New Shannon"]],
            [["T2", "M8", "H10", "M11", "T13"], ["Port Jonathan", "North Sydneyview"]],
            [["T2", "E7", "M9", "T12", "M14"], ["Omarfurt"]],
            [["M9", "H10", "M11", "T12"], ["Lawrenceland", "Meadowsberg"]],
        ],
        {
            "T2": [1, 2],
            "E7": [0, 2],
            "M8": [0, 1],
            "M9": [2, 3],
            "H10": [1, 3],
            "M11": [1, 3],
            "T12": [2, 3],
            "T13": [0, 1],
            "M14": [0, 2],
        },
    )

    map_ = read_map("examples/medium-map.csv")
    damaged_roads = read_damaged_roads("examples/medium-damaged-roads.csv")
    assert get_isolated_regions(map_, damaged_roads) == (
        [
            [
                ["T42", "M43", "E44", "E47"],
                [
                    "Port Christina",
                    "Melaniehaven",
                    "Travisburgh",
                    "North Ashleyview",
                    "Williamsville",
                    "South Alexander",
                    "Ricehaven",
                    "New Jeffreyburgh",
                ],
            ],
            [
                ["H40", "T41", "T42", "M43", "E44", "T45", "M46"],
                [
                    "New Jason",
                    "East Lindsey",
                    "South Hannahfurt",
                    "Port Michelle",
                    "South Johnstad",
                    "East Jesse",
                    "South Kristi",
                    "Alexanderchester",
                    "North Donland",
                ],
            ],
            [["H40", "T41", "M46", "E47"], ["Mortonfort", "Donaldbury", "Gloriafurt"]],
            [["T45"], ["Bestfort", "East Andrea", "Blackchester"]],
        ],
        {
            "H40": [1, 2],
            "T41": [1, 2],
            "T42": [0, 1],
            "M43": [0, 1],
            "E44": [0, 1],
            "T45": [1, 3],
            "M46": [1, 2],
            "E47": [0, 2],
        },
    )


def test_get_roads_to_recover():
    map_ = read_map("examples/small-map.csv")
    damaged_roads = read_damaged_roads("examples/small-damaged-roads.csv")
    isolated_regions = get_isolated_regions(map_, damaged_roads)
    assert get_roads_to_recover(map_, isolated_regions, damaged_roads) == {
        "M9",
        "T2",
        "M14",
    }

    map_ = read_map("examples/medium-map.csv")
    damaged_roads = read_damaged_roads("examples/medium-damaged-roads.csv")
    isolated_regions = get_isolated_regions(map_, damaged_roads)
    assert get_roads_to_recover(map_, isolated_regions, damaged_roads) == {
        "T45",
        "E47",
        "T42",
    }

    map_ = read_map("examples/large-map.csv")
    damaged_roads = read_damaged_roads("examples/large-damaged-roads.csv")
    isolated_regions = get_isolated_regions(map_, damaged_roads)
    assert get_roads_to_recover(map_, isolated_regions, damaged_roads) == {
        "T168",
        "H74",
        "H185",
        "T12",
        "E158",
        "T183",
        "H75",
        "H151",
        "T184",
        "T132",
    }
