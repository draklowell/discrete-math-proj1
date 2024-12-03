import tempfile

from rrs.datatypes import City, Map, Road
from rrs.files import read_damaged_roads, read_map


def test_read_map():
    assert read_map("examples/small-map.csv") == Map(
        roads={
            "E1": Road(city1="Port Jonathan", city2="North Sydneyview", distance=57.23),
            "T2": Road(city1="Omarfurt", city2="Port Jonathan", distance=33.11),
            "T3": Road(city1="New Shannon", city2="Deannamouth", distance=72.88),
            "T4": Road(city1="Lawrenceland", city2="Meadowsberg", distance=50.87),
            "T5": Road(city1="Meadowsberg", city2="Lawrenceland", distance=24.7),
            "E6": Road(city1="Deannamouth", city2="New Shannon", distance=65.84),
            "E7": Road(city1="New Shannon", city2="Omarfurt", distance=67.04),
            "M8": Road(city1="New Shannon", city2="North Sydneyview", distance=63.08),
            "M9": Road(city1="Meadowsberg", city2="Omarfurt", distance=29.68),
            "H10": Road(city1="North Sydneyview", city2="Lawrenceland", distance=45.45),
            "M11": Road(city1="Lawrenceland", city2="Port Jonathan", distance=92.41),
            "T12": Road(city1="Omarfurt", city2="Lawrenceland", distance=39.99),
            "T13": Road(city1="North Sydneyview", city2="New Shannon", distance=96.19),
            "M14": Road(city1="Omarfurt", city2="New Shannon", distance=42.67),
        },
        cities={
            "Port Jonathan": City(roads=["E1", "T2", "M11"]),
            "North Sydneyview": City(roads=["E1", "M8", "H10", "T13"]),
            "Omarfurt": City(roads=["T2", "E7", "M9", "T12", "M14"]),
            "New Shannon": City(roads=["T3", "E6", "E7", "M8", "T13", "M14"]),
            "Deannamouth": City(roads=["T3", "E6"]),
            "Lawrenceland": City(roads=["T4", "T5", "H10", "M11", "T12"]),
            "Meadowsberg": City(roads=["T4", "T5", "M9"]),
        },
        center="Deannamouth",
    )

    with tempfile.NamedTemporaryFile("w+", encoding="utf8") as file:
        file.write("center\n\nr1,   city1,city2  , 5.7\n\n\n")
        file.seek(0)
        assert read_map(file.name) == Map(
            roads={"r1": Road(city1="city1", city2="city2", distance=5.7)},
            cities={"city1": City(roads=["r1"]), "city2": City(roads=["r1"])},
            center="center",
        )


def test_read_damaged_roads():
    assert read_damaged_roads("examples/small-damaged-roads.csv") == {
        "T2": 3.61,
        "T4": 3.5,
        "E7": 13.77,
        "M8": 10.63,
        "M9": 5.53,
        "H10": 14.58,
        "M11": 11.61,
        "T12": 13.3,
        "T13": 6.26,
        "M14": 5.17,
    }

    with tempfile.NamedTemporaryFile("w+", encoding="utf8") as file:
        file.write("\n\nr1, 6.7\n\nr2, 8.8\n")
        file.seek(0)
        assert read_damaged_roads(file.name) == {"r1": 6.7, "r2": 8.8}
