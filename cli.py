"""
Command line interface for the RRS module.
"""

import argparse
import rrs.files
import rrs.algorithm


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
            "Path to the output file, where list of roads that are required to be repaired will be written. "
            "Default: stdout"
        ),
    )
    parser.add_argument(
        "-c",
        "--components",
        type=str,
        default="stdout",
        dest="components_path",
        help=(
            "Path to the output file, where list of isolated regions will be written. "
            "Default: stdout"
        ),
    )
    args = parser.parse_args()

    try:
        map_ = rrs.files.read_map(args.map_path)
    except FileNotFoundError:
        print("Invalid path to the map file.")

    try:
        damaged_roads = rrs.files.read_damaged_roads(args.damaged_roads_path)
    except FileNotFoundError:
        print("Invalid path to the damaged roads file.")

    isolated_regions = rrs.algorithm.get_isolated_regions(map_, damaged_roads)

    if not args.components_path or args.components_path == "stdout":
        print("Successfully found isolated regions:")
        for region in isolated_regions[0]:
            cities = ", ".join(region[1])
            print(f" - {cities}")
        print()
    else:
        with open(args.components_path, "w", encoding="utf8") as file:
            for region in isolated_regions[0]:
                cities = ", ".join(region[1])
                file.write(f"{cities}\n")
        print(
            f'Successfully found isolated regions and stored to "{args.components_path}"'
        )

    roads_to_recover = rrs.algorithm.get_roads_to_recover(
        map_, isolated_regions, damaged_roads
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
