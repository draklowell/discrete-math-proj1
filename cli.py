"""
Command line interface for the RRS module.
"""

import argparse
import graph_handling
import algorithm


def main():
    """
    Entry point for the CLI.
    """
    parser = argparse.ArgumentParser("Rapid Response Service, road services")
    parser.add_argument(
        "-m",
        "--map",
        type=str,
        dest="map_path",
        help=(
            "Path to the csv file that contains the map in the form of list of all roads, "
            "their distances and center city name."
        ),
        required=True,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        dest="damaged_roads_path",
        help=(
            "Path to the csv file that contains list of damaged roads and complexity of "
            "their repairment per km."
        ),
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="stdout",
        dest="output_path",
        help=(
            "Path to the output file, where list of roads that are required to be repaired. "
            "Default: stdout"
        ),
    )
    args = parser.parse_args()

    try:
        map_ = graph_handling.read_map(args.map_path)
    except FileNotFoundError:
        print("Invalid path to the map file.")

    try:
        damaged_roads = graph_handling.read_damaged_roads(args.damaged_roads_path)
    except FileNotFoundError:
        print("Invalid path to the damaged roads file.")

    roads_to_recover = algorithm.spanning_tree_prima(
        map_, algorithm.get_components(map_, damaged_roads), damaged_roads
    )
    if not args.output_path or args.output_path == "stdout":
        print("Successfully found best strategy to recover roads:")
        for road in roads_to_recover:
            print(f" - {road}")
    else:
        with open(args.output_path, "w", encoding="utf8") as file:
            for road in roads_to_recover:
                file.write(f"{road}\n")
        print(
            f'Successfully found best strategy to recover roads and stored to "{args.output_path}"'
        )


if __name__ == "__main__":
    main()
