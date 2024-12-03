"""
GUI for vizualization
"""
from math import pi, cos, sin
import tkinter as tk
from tkinter import filedialog

from algorithm import spanning_tree_prima, get_components, Map, Road, City
from graph_handling import read_map, read_damaged_roads

def draw_regular_polygon(canvas, center_x, center_y, radius, sides):
    """
    Function to draw regular polygon to dispaly graph
    """
    if sides < 3:
        raise ValueError("A polygon must have at least 3 sides.")

    # Calculate the angle between vertices
    angle_between_vertices = 2 * pi / sides

    # Generate the vertices of the polygon
    points = []
    for i in range(sides):
        angle = i * angle_between_vertices
        x = int(center_x + radius * cos(angle))
        y = int(center_y + radius * sin(angle))
        points.append((x, y))
    canvas.pack()
    return points

def connect_points(canvas, points, connections, color="black"):
    """
    Draws connection of the asigned dots
    """
    for start, end, status in connections:
        match status:
            case -1:
                color = "red"
            case 0:
                color = 'black'
            case 1:
                color = "blue"
        canvas.create_line(points[start][0], points[start][1],
                           points[end][0], points[end][1],
                           fill=color, width=3)

def main():
    """
    main function to assemble all the functionality
    """
    WIDTH, HEIGHT = 1500, 1000
    PADDING = 20
    RAD = 15

    window = tk.Tk()
    window.title('help me, please')
    window.geometry(f'{WIDTH}x{HEIGHT}')
    window.resizable(0,0)

    left_frame = tk.Frame(window, width=WIDTH*2//3, height=HEIGHT)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    left_frame.pack_propagate(False)
    right_frame = tk.Frame(window, width=WIDTH//4, height=HEIGHT)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    graph_canvas = tk.Canvas(left_frame, width=WIDTH, height=HEIGHT, borderwidth=0)
    graph_canvas.pack()

    filepath_map = False
    filepath_dr = False
    while not filepath_map:
        filepath_map = filedialog.askopenfilename(title="Вибери файл карти", filetypes=[("csv files only", "*.csv")])
    while not filepath_dr:
        filepath_dr = filedialog.askopenfilename(title="Вибери файл з пошкодженими дорогами", filetypes=[("csv files only", "*.csv")])

    map_ = read_map(filepath_map)
    damaged_roads = read_damaged_roads(filepath_dr)

    r = min(HEIGHT//2-PADDING, WIDTH//3-PADDING)
    points = draw_regular_polygon(graph_canvas, WIDTH//3, HEIGHT//2, r, len(map_.cities))

    connections = []
    cities = {}
    ind = 1
    for city_name, city in map_.cities.items():
        if city.is_center:
            cities[city_name] = 0
        else:
            cities[city_name] = ind
            ind += 1
    for road_name, road in map_.roads.items():
        status = -1 if road_name in damaged_roads else 0
        connections.append((cities[road.city1], cities[road.city2], status))

    connect_points(graph_canvas, points, connections)
    for i, (x, y) in enumerate(points):
        color = "GREEN" if i == 0 else "Yellow"
        graph_canvas.create_oval(x-RAD, y-RAD, x+RAD, y+RAD, fill=color)
    
    legend_canvas = tk.Canvas(right_frame, width=WIDTH//4, height=HEIGHT-70)
    legend_canvas.pack()
    oval_x1, oval_y1 = 10, 10  # Top-left corner
    oval_x2, oval_y2 = 10+2*RAD, 10+2*RAD  # Bottom-right corner
    legend_canvas.create_oval(oval_x1, oval_y1, oval_x2, oval_y2, fill="green", outline="black")
    legend_canvas.create_oval(oval_x1, oval_y1+oval_y2, oval_x2, oval_y2*2, fill="yellow", outline="black")

    # Add label for the green oval
    label_x, label_y = 2*(oval_x1 + oval_x2), (oval_y2+oval_y1)//2
    legend_canvas.create_text(label_x, label_y, text="Center city", font=("Arial", 12), fill="black")
    legend_canvas.create_text(label_x, (3*oval_y2+oval_y1)//2, text="Regular city", font=("Arial", 12), fill="black")

    road_legend = 'Red line - broken road\nBlack line - normal road\nBlue road - road that needs to be repaired'
    legend_canvas.create_text(3*(oval_x1+oval_x2), (3*oval_y2+oval_y1)//2+4*RAD, text=road_legend, font=("Arial", 12), fill="black")

    def clicked():
        roads = spanning_tree_prima(map_, get_components(map_, damaged_roads), damaged_roads)
        connections = []
        for road in roads:
            road = map_.roads[road]
            connections.append((cities[road.city1], cities[road.city2], 1))
        connect_points(graph_canvas, points, connections)
        for i, (x, y) in enumerate(points):
            color = "GREEN" if i == 0 else "Yellow"
            graph_canvas.create_oval(x-RAD, y-RAD, x+RAD, y+RAD, fill=color)
        

    button = tk.Button(right_frame, text="Порахувати", command=clicked, font=("Arial", 25))
    button.pack(side=tk.BOTTOM, pady=10)

    tk.mainloop()

if __name__ == '__main__':
    main()
