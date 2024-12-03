"""
GUI for vizualization
"""
import tkinter as tk
from tkinter import filedialog

import pydot

from algorithm import spanning_tree_prima, get_components, Map
from graph_handling import read_map, read_damaged_roads

def create_graph(map_:Map, damaged_roads:dict, repaired_roads:list[str]=None) -> str:
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
        color = "green" if map_.cities[city].is_center else "yellow"
        graph.add_node(pydot.Node(city, style="filled", fillcolor=color))

    # creating edges
    for road_name, road in map_.roads.items():
        if repaired_roads is not None and road_name in repaired_roads:
            color = "green"
        elif road_name in damaged_roads:
            color = "red"
        else:
            color = "black"
        graph.add_edge( pydot.Edge(road.city1, road.city2, label=road_name, \
                                   weight=road.distance, color=color, penwidth="3") )

    file_name = "input.png" if repaired_roads is None else "output.png"

    graph.write_png(file_name)

    return file_name

def main():
    """
    Just main function \_0_/
    """
    WIDTH, HEIGHT = 1400, 900
    font = ("Arial", 25)

    window = tk.Tk()
    window.title('help me, please')
    window.geometry(f'{WIDTH}x{HEIGHT}')
    window.resizable(0,0)
    window.configure(background='white')

    right_frame = tk.Frame(window, bg="white")
    right_frame.pack(side=tk.RIGHT, pady=10, padx=10)
    left_frame = tk.Frame(window, bg="white")
    left_frame.pack(side=tk.LEFT, pady=10, padx=10)

    filepath_map = False
    filepath_dr = False
    while not filepath_map:
        filepath_map = filedialog.askopenfilename(title="Вибери файл карти", \
                                                  filetypes=[("csv files only", "*.csv")])
    while not filepath_dr:
        filepath_dr = filedialog.askopenfilename(title="Вибери файл з пошкодженими дорогами", \
                                                 filetypes=[("csv files only", "*.csv")])

    map_ = read_map(filepath_map)
    damaged_roads = read_damaged_roads(filepath_dr)

    img = tk.PhotoImage(file=create_graph(map_, damaged_roads))
    label = tk.Label(left_frame, image=img)
    label.pack(pady=10)

    legend_txt = "Зелений колір - обласний центр\nЖовтий колір - населений пункт\n\n\
Червона лінія - поламана дорога між містами\nЧорна лінія - функціонуюча дорога між містами\
\nЗелена лінія - дорога яку слід відремонтувати"
    tk.Label(right_frame, text=legend_txt, font=font, bg='white').pack(side=tk.TOP, pady = 10)

    def clicked(label):
        roads = spanning_tree_prima(map_, get_components(map_, damaged_roads), damaged_roads)
        global img
        img = tk.PhotoImage(file=create_graph(map_, damaged_roads, roads))
        label.config(image=img)
        tk.Label(right_frame, text=f"Дороги які слід відремонтувати: {roads}", \
font=font,background='white').pack(side=tk.TOP, pady=10)
    button = tk.Button(right_frame, text="Порахувати", command=lambda: \
clicked(label), font=("Arial", 25))
    button.pack(side=tk.TOP, pady=10)

    tk.mainloop()

if __name__ == '__main__':
    main()
