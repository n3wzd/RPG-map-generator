import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import dungeon_maker
import map_to_image
import map_to_json
import parameter as param
import tile_crop
import tile_rule as tile

map_type_dispaly = ["Dungeon", "Cave", "Plain", "Field"]
map_type_value = [0, 1, 2, 3]
map_type_map = dict(zip(map_type_dispaly, map_type_value))
output_path = 'output/'
tileset = tile_crop.main(1)

def get_all_tileset():
    return tile_crop.main(1)

def validate_range(value, min_value, max_value):
    try:
        if min_value <= int(value) <= max_value:
            return True
        else:
            return False
    except ValueError:
        return False

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x}+{y}")

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Map Generator")
        self.root.resizable(False, False)
        center_window(root, 1500, 800)

        # Left Side
        def update_checkboxes(event):
            value = map_type_map[self.map_type.get()]
            for i in range(4):
                if value == i:
                    sidebar_left_sub[i].pack()
                else:
                    sidebar_left_sub[i].pack_forget()

        sidebar_left = tk.Frame(root, padx=10, pady=10)
        sidebar_left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar_left, text="Parameters", font=("Arial", 16)).pack(pady=(0, 10))

        tk.Label(sidebar_left, text="Map Type").pack(anchor=tk.W)
        self.map_type = tk.StringVar()
        map_type_menu = ttk.Combobox(sidebar_left, textvariable=self.map_type, values=map_type_dispaly, state="readonly")
        map_type_menu.set(map_type_dispaly[0])
        map_type_menu.bind("<<ComboboxSelected>>", update_checkboxes)
        map_type_menu.pack()

        self.map_width = self.create_number_field(sidebar_left, "Map Width", 10, 300, 48)
        self.map_height = self.create_number_field(sidebar_left, "Map Height", 10, 300, 48)
        self.map_padding = self.create_slider(sidebar_left, "Map Padding", 0, 9, 4)
        self.wall_height = self.create_slider(sidebar_left, "Wall Height", 1, 9, 2)

        sidebar_left_sub_base = tk.Frame(sidebar_left, pady=10)
        sidebar_left_sub_base.pack()
        sidebar_left_sub = []
        for i in range(4):
            sidebar_left_sub.append(tk.Frame(sidebar_left_sub_base))
        sidebar_left_sub[0].pack()
        
        self.room_min_size, self.room_max_size = self.create_range_slider(sidebar_left_sub[0], "Room Min Size", "Room Max Size", 0, 100, 25, 50, False)
        self.room_padding = self.create_slider(sidebar_left_sub[0], "Room Padding", 0, 100, 0, False)
        self.corridor_wide_auto = self.create_switch(sidebar_left_sub[0], "Auto Corridor Wide", False)
        self.corridor_wide = self.create_slider(sidebar_left_sub[0], "Corridor Wide", 0, 100, 50, False)
        self.room_freq = self.create_slider(sidebar_left_sub[0], "Room Frequency", 0, 100, 50, False)

        self.wall_probability = self.create_slider(sidebar_left_sub[1], "Wall Frequency", 400, 600, 500, False)
        self.cellular_iterations = self.create_slider(sidebar_left_sub[1], "Terrain Smoothness", 1, 10, 4, False)
        
        self.path_random_factor = self.create_slider(sidebar_left_sub[2], "Path Randomness", 0, 5, 3, False)
        self.house_num = self.create_slider(sidebar_left_sub[2], "Number of House", 0, 15, 3)
        self.town_boundary_margin = self.create_slider(sidebar_left_sub[2], "Town Padding", 0, 9, 3)
        
        self.perlin_scale = self.create_slider(sidebar_left_sub[3], "Terrain Complexity", 50, 200, 100, False)
        self.elevation_level = self.create_slider(sidebar_left_sub[3], "Elevation Level", 0, 3, 1)

        tk.Button(sidebar_left, text="Generate", command=self.on_submit).pack(side=tk.BOTTOM)

        # Right
        sidebar_right = tk.Frame(root, padx=10, pady=10)
        sidebar_right.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(sidebar_right, text="Tiles", font=("Arial", 16)).pack(pady=(0, 10))
        self.tile_tree = ttk.Treeview(sidebar_right, columns=("text", "image"), show="tree")
        self.tile_tree.column("text", width=80)
        self.tile_tree.column("image", width=48)
        self.tile_tree.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=48)

        self.tile_tree_image = {}
        self.insert_tree_button("floor", tile.floor)
        self.insert_tree_button("wall", tile.wall)
        self.insert_tree_button("ceil", tile.ceil)
        self.insert_tree_button("blank", tile.blank)
        self.insert_tree_button("path", tile.path)
        self.insert_tree_button("cover_0", tile.floor_cover[0].id, tile.floor)
        self.insert_tree_button("cover_1", tile.floor_cover[1].id, tile.floor)
        self.insert_tree_button("cover_2", tile.floor_cover[2].id, tile.floor)
        self.insert_tree_button("cover_3", tile.floor_cover[3].id, tile.floor)
        self.insert_tree_button("extra_0", tile.extra[0].base.id)
        self.insert_tree_button("extra_1", tile.extra[1].base.id)
        self.insert_tree_button("extra_2", tile.extra[2].base.id)
        self.insert_tree_button("extra_3", tile.extra[3].base.id)

        def on_tree_item_click(event):
            item_id = self.tile_tree.identify_row(event.y)
            if item_id != "" and event.x > 20:
                self.open_tile_selection_window(self.tile_tree.item(item_id, "values")[0], item_id)

        self.tile_tree.bind("<Button-1>", on_tree_item_click)

        # Center
        self.main_content = tk.Frame(root, padx=10, pady=10)
        self.main_content.pack(fill=tk.BOTH, expand=True)

        self.result_image = tk.Label(self.main_content, text="Press generate button to create map!")
        self.result_image.pack(fill=tk.BOTH, expand=True)


    def create_number_field(self, parent, label, min_val, max_val, default_val):
        def on_validate_input(*args):
            value = entry_var.get()
            if validate_range(value, min_val, max_val):
                entry.config(bg='white')
            else:
                entry.config(bg='red')

        frame = tk.Frame(parent)
        frame.pack(pady=(15, 0))
        tk.Label(frame, text=label).pack(anchor=tk.W)
        entry_var = tk.StringVar()
        entry_var.trace_add("write", on_validate_input)
        entry = tk.Entry(frame, textvariable=entry_var)
        entry.insert(0, default_val)
        entry.pack()
        return entry

    def create_slider(self, parent, label, min_val, max_val, default_val, showvalue=True):
        frame = tk.Frame(parent)
        frame.pack(pady=(15, 0))
        tk.Label(frame, text=label).pack(anchor=tk.W)
        slider = tk.Scale(frame, from_=min_val, to=max_val, orient=tk.HORIZONTAL, showvalue=showvalue)
        slider.set(default_val)
        slider.pack()
        return slider

    def create_range_slider(self, parent, label1, label2, min_val, max_val, default_val1, default_val2, showvalue=True):
        def on_min_scale_change(value):
            v1, v2 = (int(slider1.get()), int(slider2.get()))
            if v1 > v2:
                slider2.set(v1)
                
        def on_max_scale_change(value):
            v1, v2 = (int(slider1.get()), int(slider2.get()))
            if v1 > v2:
                slider1.set(v2)
            
        slider1 = self.create_slider(parent, label1, min_val, max_val, default_val1, showvalue)
        slider2 = self.create_slider(parent, label2, min_val, max_val, default_val2, showvalue)
        slider1.config(command=on_min_scale_change)
        slider2.config(command=on_max_scale_change)
        return (slider1, slider2)

    def create_switch(self, parent, label, default_val):
        frame = tk.Frame(parent)
        frame.pack(pady=(15, 0))
        tk.Label(frame, text=label).pack(anchor=tk.W)
        switch = tk.BooleanVar(value=default_val)
        checkbutton = tk.Checkbutton(frame, variable=switch)
        checkbutton.pack()
        return switch

    def open_tile_selection_window(self, title, tile_key):
        grid_width = 8
        grid_height = 16
        tiles = []

        def on_tile_click(row, col):
            param.theme[int(tile_key)] = 2048 + 48 * (col + row * grid_width)
            self.update_tree_button(tile_key)
            new_window.destroy()

        new_window = tk.Toplevel(root)
        new_window.title(title)
        new_window.resizable(False, False)
        center_window(new_window, 450, 600)
        
        outer_frame = tk.Frame(new_window)
        outer_frame.place(x=0, y=0, relwidth=1, relheight=1)
        canvas = tk.Canvas(outer_frame, bg="lightgrey")
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        row_cnt = 0
        wall_row = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1]
        for row in range(grid_height):
            row_tiles = []
            for col in range(grid_width):
                photo = ImageTk.PhotoImage(tileset[2048 + 48 * (col + row * grid_width)])
                tile_button = tk.Button(scrollable_frame, image=photo, relief="flat", command=lambda r=row, c=col: on_tile_click(r, c), bg="lightgrey")
                tile_button.grid(row=row_cnt, column=col)
                tile_button.image = photo
                row_tiles.append(tile_button)
            tiles.append(row_tiles)
            if(wall_row[row] == bool(tile_key == str(tile.wall))):
                row_cnt += 1

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_columnconfigure(0, weight=1)

    def update_tree_button(self, tile_key):
        photo = ImageTk.PhotoImage(tileset[param.theme[int(tile_key)]])
        self.tile_tree.item(tile_key, image=photo)
        self.tile_tree_image[tile_key] = photo

    def insert_tree_button(self, label, tile_key, parent=""):
        photo = ImageTk.PhotoImage(tileset[param.theme[int(tile_key)]])
        self.tile_tree.insert(parent, "end", tile_key, values=(label, ""), image=photo)
        self.tile_tree_image[tile_key] = photo

    def update_image(self, img_path):
        width = self.result_image.winfo_width()
        height = self.result_image.winfo_height()

        image = Image.open(img_path).resize((width, height))
        photo = ImageTk.PhotoImage(image)

        self.result_image.config(image=photo)
        self.result_image.image = photo

    def on_submit(self):
        def setParam(key, value):
            if hasattr(param, key):
                setattr(param, key, value)
                
        def mappedValue(v, a, b):
            return int(int(a) + (float(v) / 100) * (int(b) - int(a)));
        
        if(not validate_range(self.map_width.get(), 10, 300)):
            return
        if(not validate_range(self.map_height.get(), 10, 300)):
            return

        self.result_image.text = "Generating..."

        setParam('map_type', map_type_map[self.map_type.get()])
        setParam('map_width', int(self.map_width.get()))
        setParam('map_height', int(self.map_height.get()))
        setParam('map_padding', int(self.map_padding.get()))
        setParam('wall_height', int(self.wall_height.get()))
        
        room_size_limit = min(int(self.map_width.get()), int(self.map_height.get())) - int(self.map_padding.get())
        setParam('room_min_size', mappedValue(self.room_min_size.get(), 4, room_size_limit))
        setParam('room_max_size', mappedValue(self.room_max_size.get(), 4, room_size_limit))
        setParam('room_padding', mappedValue(self.room_padding.get(), 0, int(self.room_min_size.get()) // 2))
        setParam('corridor_wide_auto', self.corridor_wide_auto.get())
        setParam('corridor_wide', mappedValue(self.corridor_wide.get(), 1, (int(self.room_min_size.get()) - int(self.wall_height.get())) // 2))
        setParam('room_freq', float(self.room_freq.get()) / 100)

        setParam('wall_probability', float(self.wall_probability.get()) / 1000)
        setParam('cellular_iterations', int(self.cellular_iterations.get()))

        setParam('path_random_factor', int(self.path_random_factor.get()))
        setParam('house_num', int(self.house_num.get()))
        setParam('town_boundary_margin', int(self.town_boundary_margin.get()))
        
        setParam('perlin_scale', int(self.perlin_scale.get()))
        setParam('elevation_level', int(self.elevation_level.get()))

        dungeon = dungeon_maker.main()
        img_path = map_to_image.main(dungeon.map, tileset, param.map_id, output_path)
        map_to_json.main(dungeon.map, param.tileset_id, param.map_id, output_path)

        self.update_image(img_path)


root = tk.Tk()
app = GUI(root)
root.mainloop()
