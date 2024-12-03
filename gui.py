"""
GUI for vizualization
"""

import tkinter as tk
from tkinter import filedialog

import pydot
from PIL import Image, ImageTk

from rrs.algorithm import get_isolated_regions, get_roads_to_recover
from rrs.datatypes import Map
from rrs.files import read_damaged_roads, read_map


def create_graph(
    map_: Map, damaged_roads: dict, repaired_roads: list[str] = None
) -> str:
    """
    Creates an image of graph with damaged and repaired roads

    :param map_: Map, graph as it is
    :param damaged_roads: dict, key is a name of a road and value is price for repaire
    :param repaired_roads: list, list of names of repaired roads. If not given, equals None
    :return: str, name of file with image of a graph
    """

    graph = pydot.Dot("Cities", graph_type="graph")

    # creating nodes
    for city in map_.cities:
        color = "green" if map_.center == city else "yellow"
        graph.add_node(pydot.Node(city, style="filled", fillcolor=color))

    # creating edges
    for road_name, road in map_.roads.items():
        if repaired_roads is not None and road_name in repaired_roads:
            color = "green"
        elif road_name in damaged_roads:
            color = "red"
        else:
            color = "black"
        graph.add_edge(
            pydot.Edge(
                road.city1,
                road.city2,
                label=road_name,
                weight=road.distance,
                color=color,
                penwidth="3",
            )
        )

    file_name = "input.png" if repaired_roads is None else "output.png"

    graph.write_png(file_name)

    return file_name


def resize_image_to_fit_frame(
    image_path: str, frame_width: int, frame_height: int
) -> ImageTk.PhotoImage:
    """
    Read image from the given path and resize it to the given size.

    :param image_path: str, path to the image
    :param frame_width: int, desired width of the image
    :param frame_height: int, desired height of the image

    :returns: PhotoImage, image suitable for the tkinter
    """
    # Open the image
    image = Image.open(image_path)

    # Resize the image while maintaining its aspect ratio
    image_ratio = image.width / image.height
    frame_ratio = frame_width / frame_height

    if image_ratio > frame_ratio:
        # Fit to width
        new_width = frame_width
        new_height = int(frame_width / image_ratio)
    else:
        # Fit to height
        new_height = frame_height
        new_width = int(frame_height * image_ratio)

    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_image)


WIDTH, HEIGHT = 1600, 1000
FONT = "Arial"


def main():
    """
    Entry point for the CLI.
    """
    window = tk.Tk()
    window.title("help me, please")
    window.geometry(f"{WIDTH}x{HEIGHT}")
    window.resizable(0, 0)
    window.configure(background="white")

    right_frame = tk.Frame(window, bg="white", width=WIDTH // 2, height=HEIGHT // 2)
    right_frame.pack(side=tk.RIGHT, pady=10, padx=10)
    left_frame = tk.Frame(window, bg="white", width=WIDTH // 2, height=HEIGHT // 2)
    left_frame.pack(side=tk.LEFT, pady=10, padx=10)

    filepath_map = False
    filepath_dr = False
    while not filepath_map:
        filepath_map = filedialog.askopenfilename(
            title="Вибери файл карти", filetypes=[("csv files only", "*.csv")]
        )
    while not filepath_dr:
        filepath_dr = filedialog.askopenfilename(
            title="Вибери файл з пошкодженими дорогами",
            filetypes=[("csv files only", "*.csv")],
        )

    map_ = read_map(filepath_map)
    damaged_roads = read_damaged_roads(filepath_dr)

    image = resize_image_to_fit_frame(
        create_graph(map_, damaged_roads), WIDTH // 2, HEIGHT // 2
    )

    label = tk.Label(left_frame, image=image)
    label.pack(pady=10, padx=30)

    legend_txt = (
        "Зелений колір - обласний центр\nЖовтий колір - населений пункт\n\n"
        "Червона лінія - поламана дорога між містами\nЧорна лінія - функціонуюча дорога між містами"
        "\nЗелена лінія - дорога яку слід відремонтувати"
    )
    tk.Label(right_frame, text=legend_txt, font=(FONT, 23), bg="white").pack(
        side=tk.TOP, pady=10, padx=10
    )

    def clicked(label):
        roads = get_roads_to_recover(
            map_, get_isolated_regions(map_, damaged_roads), damaged_roads
        )

        global image
        image = resize_image_to_fit_frame(
            create_graph(map_, damaged_roads, roads), WIDTH // 2, HEIGHT // 2
        )

        label.config(image=image)

        tk.Label(
            right_frame,
            text=f"Дороги які слід відремонтувати: {roads}",
            font=(FONT, 15),
            background="white",
        ).pack(side=tk.TOP, pady=10, padx=10)

    button = tk.Button(
        right_frame,
        text="Порахувати",
        command=lambda: clicked(label),
        font=(FONT, 23),
    )
    button.pack(side=tk.TOP, pady=10, padx=10)

    tk.mainloop()


if __name__ == "__main__":
    main()
