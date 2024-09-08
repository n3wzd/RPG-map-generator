import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import pickle

import dungeon_maker
import map_to_image
import map_to_json
import parameter as param
import setting
import tile_crop
import tile_rule as tile

tileset = tile_crop.main()

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

def transform_dimension(v, a, b, c, d):
    return int(c + (v - a) / (b - a) * (d - c))

def boundary_check(min_val, max_val, value):
    return min(max_val, max(min_val, value))

class GUI:
    def __init__(self, root):
        setting.load_ini()

        self.root = root
        self.root.title("RPG Map Generator")
        self.root.resizable(False, False)
        center_window(root, 1500, 900)

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=48)
        
        style.configure("TButton",
                        background="#333333",
                        foreground="white",
                        font=("Arial", 16),
                        borderwidth=2,
                        focusthickness=3,
                        focuscolor="none",
                        relief="flat")

        style.map("TButton",
                        background=[("active", "#444444"), ("pressed", "#222222")])

        style.configure("TScale",
                        troughcolor="#DDDDDD",
                        background="#FFFFFF",
                        gripcolor="#DDDDDD",
                        borderwidth=0)   


        # Structure
        self.map_entry = {}
        self.map_slider = {}
        self.map_switch = {}
        self.submit_active = {}

        # Top Side
        top_bar = tk.Frame(root, bg="lightgrey", height=50)
        top_bar.pack(side="top", fill="x")

        self.submit_btn = ttk.Button(top_bar, text="Generate", command=self.on_submit, style="TButton")
        self.submit_btn.pack(side=tk.LEFT)
        ttk.Button(top_bar, text="Save", command=self.save_single_file, style="TButton").pack(side=tk.LEFT)
        ttk.Button(top_bar, text="Load", command=self.load_single_file, style="TButton").pack(side=tk.LEFT)

        # Left Side
        sidebar_left = tk.Frame(root, padx=10, pady=10)
        sidebar_left.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar_left, text="Parameters", font=("Arial", 16)).pack(pady=(0, 10))

        def update_tileset_type(event):  
            self.update_tree_items()
            param.tileset_type = self.tileset_type.get()

        tk.Label(sidebar_left, text="Tileset").pack(anchor=tk.W)
        self.tileset_type = tk.StringVar()
        self.tileset_type_menu = ttk.Combobox(sidebar_left, textvariable=self.tileset_type, values=tile_crop.tileset_key, state="readonly")
        self.tileset_type_menu.bind("<<ComboboxSelected>>", update_tileset_type)
        self.tileset_type_menu.pack(pady=(5, 10))

        def update_sidebar_left_sub(value):
            for i in range(4):
                if value == i:
                    sidebar_left_sub[i].pack()
                else:
                    sidebar_left_sub[i].pack_forget()

        def update_map_type(event):
            update_sidebar_left_sub(param.map_type_map[self.map_type.get()])
        
        self.map_type = tk.StringVar()
        self.map_type_menu = ttk.Combobox(sidebar_left, textvariable=self.map_type, values=param.map_type_dispaly, state="readonly")
        self.map_type_menu.bind("<<ComboboxSelected>>", update_map_type)
        self.map_type_menu.pack(pady=(5, 10))

        self.create_number_field(sidebar_left, "Tileset ID", "tileset_id")
        self.create_number_field(sidebar_left, "Map ID", "map_id")
        self.create_number_field(sidebar_left, "Map Width", "map_width")
        self.create_number_field(sidebar_left, "Map Height", "map_height")
        self.create_number_field(sidebar_left, "Map Padding", "map_padding")
        self.create_number_field(sidebar_left, "Wall Height", "wall_height")
        self.create_slider(sidebar_left, "Decoration Rate", "deco_rate", False)
        ttk.Separator(sidebar_left, orient='horizontal').pack(fill='x', pady=(10, 0))
        
        tk.Label(sidebar_left, text="Graph", font=("Arial", 12)).pack()
        self.create_number_field(sidebar_left, "Number of Vertex", "house_num")
        self.create_slider(sidebar_left, "Edge Randomness", "path_random_factor", False)
        ttk.Separator(sidebar_left, orient='horizontal').pack(fill='x', pady=(10, 0))

        sidebar_left_sub_base = tk.Frame(sidebar_left)
        sidebar_left_sub_base.pack()
        sidebar_left_sub = []
        for i in range(4):
            sidebar_left_sub.append(tk.Frame(sidebar_left_sub_base))
        sidebar_left_sub[0].pack()
        
        tk.Label(sidebar_left_sub[0], text="Dungeon", font=("Arial", 12)).pack()
        self.create_range_slider(sidebar_left_sub[0], "Room Min Size", "Room Max Size", "room_min_size", "room_max_size")
        self.create_slider(sidebar_left_sub[0], "Room Padding", "room_padding", False)
        self.create_switch(sidebar_left_sub[0], "Auto Corridor Wide", "corridor_wide_auto")
        self.create_slider(sidebar_left_sub[0], "Corridor Wide", "corridor_wide", False)
        self.create_slider(sidebar_left_sub[0], "Room Frequency", "room_freq", False)

        tk.Label(sidebar_left_sub[1], text="Cave", font=("Arial", 12)).pack()
        self.create_slider(sidebar_left_sub[1], "Wall Frequency", "wall_probability", False)
        self.create_slider(sidebar_left_sub[1], "Terrain Smoothness", "cellular_iterations", False)
        
        tk.Label(sidebar_left_sub[3], text="Field", font=("Arial", 12)).pack()
        self.create_slider(sidebar_left_sub[3], "Terrain Complexity", "perlin_scale", False)
        self.create_slider(sidebar_left_sub[3], "Elevation Level", "elevation_level")

        # Right
        sidebar_right = tk.Frame(root, padx=10, pady=10)
        sidebar_right.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(sidebar_right, text="Tiles", font=("Arial", 16)).pack(pady=(0, 10))
        self.tile_tree = ttk.Treeview(sidebar_right, columns=("text", "image"), show="tree")
        self.tile_tree.column("text", width=80)
        self.tile_tree.column("image", width=48)
        self.tile_tree.pack(fill="both", expand=True)

        self.tile_tree_image = {}
        self.insert_tree_button("floor", tile.floor)
        self.insert_tree_button("wall", tile.wall)
        self.insert_tree_button("ceil", tile.ceil)
        self.insert_tree_button("path", tile.path)
        self.insert_tree_button("vertex", tile.vertex)
        self.insert_tree_button("cover_0", tile.floor_cover[0].id, tile.floor)
        self.insert_tree_button("cover_1", tile.floor_cover[1].id, tile.floor)
        self.insert_tree_button("cover_2", tile.floor_cover[2].id, tile.floor)
        self.insert_tree_button("cover_3", tile.floor_cover[3].id, tile.floor)
        self.insert_tree_button("extra_0", tile.extra[0].base.id)
        self.insert_tree_button("extra_1", tile.extra[1].base.id)
        self.insert_tree_button("extra_2", tile.extra[2].base.id)
        self.insert_tree_button("extra_3", tile.extra[3].base.id)

        insert_tree_menu = tk.Menu(root, tearoff=0)
        insert_tree_menu.add_command(label="Reset")

        def on_tree_right_click(event):
            def reset_item(tile_key):
                param.theme[int(tile_key)] = 0
                self.update_tree_button(tile_key)

            item_id = self.tile_tree.identify_row(event.y)
            if item_id != "" and int(item_id) not in [tile.floor, tile.wall, tile.ceil, tile.path]:
                self.tile_tree.selection_set(item_id)
                insert_tree_menu.entryconfig("Reset", command=lambda: reset_item(item_id))
                insert_tree_menu.post(event.x_root, event.y_root)

        def on_tree_item_click(event):
            item_id = self.tile_tree.identify_row(event.y)
            if item_id != "" and event.x > 20:
                self.open_tile_selection_window(self.tile_tree.item(item_id, "values")[0], item_id)

        self.tile_tree.bind("<Button-3>", on_tree_right_click)
        self.tile_tree.bind("<Button-1>", on_tree_item_click)
        
        self.decotile_tree = ttk.Treeview(sidebar_right, columns=("text"), show="tree")
        self.decotile_tree.pack(fill=tk.BOTH, expand=True)
        self.insert_decotree_button("floor_deco", tile.floor)
        self.insert_decotree_button("wall_deco", tile.wall)

        def on_decotree_item_click(event):
            item_id = self.decotile_tree.identify_row(event.y)
            if item_id != "":
                self.open_tile_selection_window(self.decotile_tree.item(item_id, "values"), 0, True, int(item_id))

        self.decotile_tree.bind("<Button-1>", on_decotree_item_click)

        # Center
        main_content = tk.Frame(root, padx=10, pady=10)
        main_content.pack(fill=tk.BOTH, expand=True)

        self.result_image = tk.Label(main_content, font=("Arial", 12), text="Press generate button to create map!")
        self.result_image.pack(fill=tk.BOTH, expand=True)

        self.update_UI()

    def update_submit_btn_active(self):
        self.submit_btn.config(state=("normal" if all(self.submit_active.values()) else "disabled"))

    def get_tile_image(self, tile_id):
        photo = None
        if self.tileset_type.get() in tile_crop.tileset_key:
            photo = ImageTk.PhotoImage(tileset[self.tileset_type.get()][tile_id])
        else:
            photo = ImageTk.PhotoImage(Image.new('RGBA', (param.TILE_PX_SIZE, param.TILE_PX_SIZE), (0, 0, 0, 0)))
        return photo

    def create_switch(self, parent, label, key):
        frame = tk.Frame(parent)
        frame.pack(pady=(15, 0))
        tk.Label(frame, text=label).pack(anchor=tk.W)
        switch = tk.BooleanVar()
        checkbutton = tk.Checkbutton(frame, variable=switch)
        checkbutton.pack()
        self.map_switch[key] = switch
        return switch

    def create_number_field(self, parent, label, key):
        min_val, max_val = param.boundary[key]()

        def on_validate_input(*args):
            value = entry_var.get()
            if validate_range(value, min_val, max_val):
                entry.config(bg="white")
                self.submit_active[label] = True
            else:
                entry.config(bg="lightyellow")
                self.submit_active[label] = False
            self.update_submit_btn_active()
            if len(value) > 6:
                entry_var.set(value[:6])

        frame = tk.Frame(parent)
        frame.pack(pady=(10, 0), fill="x")
        tk.Label(frame, text=label).pack(anchor=tk.W, side="left")
        
        entry_var = tk.StringVar()
        entry_var.trace_add("write", on_validate_input)
        entry = tk.Entry(frame, textvariable=entry_var, width=8)
        entry.pack(side="right")
        
        self.map_entry[key] = entry
        self.submit_active[label] = True
        return entry
        

    def create_slider(self, parent, label, key, showvalue=True):
        frame = tk.Frame(parent)
        frame.pack(pady=(10, 0))
        tk.Label(frame, text=label).pack(anchor=tk.W)
        slider = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, style="TScale")
        slider.pack(side='right')
        slider_label = tk.Label(frame)
        if showvalue:
            slider_label.pack(side='right')
            
        def update_label(value):
            slider_label.config(text=int(float(value)))
        slider.config(command=update_label)
        self.map_slider[key] = slider
        return slider

    def create_range_slider(self, parent, label1, label2, key1, key2):
        def on_min_scale_change(value):
            v1, v2 = (int(slider1.get()), int(slider2.get()))
            if v1 > v2:
                slider2.set(v1)
                
        def on_max_scale_change(value):
            v1, v2 = (int(slider1.get()), int(slider2.get()))
            if v1 > v2:
                slider1.set(v2)
            
        slider1 = self.create_slider(parent, label1, key1, False)
        slider2 = self.create_slider(parent, label2, key2, False)
        slider1.config(command=on_min_scale_change)
        slider2.config(command=on_max_scale_change)
        return (slider1, slider2)

    def open_tile_selection_window(self, title, tile_key, is_deco=False, tile_target=0):
        grid_width = 8
        grid_height = 64 if is_deco else 16
        tile_const = 0 if is_deco else 2048

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

        if is_deco:
            def on_tile_click(row, col):
                key = tile_const + (col + row * grid_width)
                if param.tilegen_normal[int(tile_target)][key] > 0:
                    param.tilegen_normal[int(tile_target)][key] = 0
                    grid_button[row][col].config(bg="lightgrey")
                else:
                    param.tilegen_normal[int(tile_target)][key] = 1
                    grid_button[row][col].config(bg="yellow")

            grid_button = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
            for row in range(grid_height):
                for col in range(grid_width):
                    photo = self.get_tile_image(tile_const + (col + row * grid_width))
                    grid_button[row][col] = tk.Button(scrollable_frame, image=photo, relief="flat", command=
                        lambda r=row, c=col: on_tile_click(r, c), bg="lightgrey")
                    grid_button[row][col].grid(row=row, column=col)
                    grid_button[row][col].image = photo
                    if param.tilegen_normal[int(tile_target)][tile_const + (col + row * grid_width)] > 0:
                        grid_button[row][col].config(bg="yellow")  
        else:
            row_cnt = 0
            wall_row = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1]
            tile_adder = 0 if tile_key == str(tile.wall) else 47

            def on_tile_click(row, col):
                param.theme[int(tile_key)] = tile_const + 48 * (col + row * grid_width)
                self.update_tree_button(tile_key)
                new_window.destroy()

            for row in range(grid_height):
                row_tiles = []
                for col in range(grid_width):
                    photo = self.get_tile_image(tile_const + 48 * (col + row * grid_width) + tile_adder)
                    tile_button = tk.Button(scrollable_frame, image=photo, relief="flat", command=lambda r=row, c=col: on_tile_click(r, c), bg="lightgrey")
                    tile_button.grid(row=row_cnt, column=col)
                    tile_button.image = photo
                
                if wall_row[row] == int(tile_key == str(tile.wall)):
                    row_cnt += 1

        scrollable_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        new_window.grid_rowconfigure(0, weight=1)
        new_window.grid_columnconfigure(0, weight=1)

    def update_tree_items(self, parent=''):
        children = self.tile_tree.get_children(parent)
        for child in children:
            self.update_tree_button(child)
            self.update_tree_items(child)

    def update_tree_button(self, tile_key):
        adder = 0 if tile_key == str(tile.wall) or param.theme[int(tile_key)] < 2048 else 47
        photo = self.get_tile_image(param.theme[int(tile_key)] + adder)
        self.tile_tree.item(tile_key, image=photo)
        self.tile_tree_image[tile_key] = photo

    def insert_tree_button(self, label, tile_key, parent=""):
        photo = self.get_tile_image(param.theme[int(tile_key)])
        self.tile_tree.insert(parent, "end", tile_key, values=(label, ""), image=photo)
        self.tile_tree_image[tile_key] = photo
        
    def insert_decotree_button(self, label, tile_target):
        self.decotile_tree.insert("", "end", tile_target, values=label)

    def update_dungeon_image(self, img_path):
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

        self.result_image.config(text="Generating...", image="")
        self.result_image.image=""
        root.update()

        setParam('tileset_type', self.tileset_type.get())
        setParam('map_type', param.map_type_map[self.map_type.get()])

        for key, entry in self.map_entry.items():
            setParam(key, int(entry.get()))

        for key, slider in self.map_slider.items():
            min_val, max_val = param.boundary[key]()
            setParam(key, transform_dimension(int(slider.get()), 0, 100, min_val, max_val))
            
        for key, switch in self.map_switch.items():
            setParam(key, switch.get())

        dungeon = dungeon_maker.main()
        img_path = map_to_image.main(dungeon.map, tileset[param.tileset_type], param.map_id, param.output_path)
        map_to_json.main(dungeon.map, param.tileset_id, param.map_id, param.output_path)

        self.update_dungeon_image(img_path)
        setting.save_ini()
        
    def update_UI(self):
        if param.tileset_type in tile_crop.tileset_key:
            self.tileset_type_menu.set(param.tileset_type)
        self.map_type_menu.set(param.map_type_dispaly[boundary_check(0, 3, param.map_type)])
            
        for key, entry in self.map_entry.items():
            min_val, max_val = param.boundary[key]()
            val = getattr(param, key)
            entry.delete(0, tk.END)
            entry.insert(0, boundary_check(min_val, max_val, val))

        for key, slider in self.map_slider.items():
            min_val, max_val = param.boundary[key]()
            val = getattr(param, key)
            slider.set(transform_dimension(boundary_check(min_val, max_val, val), min_val, max_val, 0, 100))
        
        for key, switch in self.map_switch.items():
            val = getattr(param, key)
            switch.set(val)

        self.update_tree_items()
        self.update_submit_btn_active()

    def save_single_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bin",
            initialfile="save.bin",
            filetypes=[("All files", "*.*")],
            title="Save file"
        )

        if file_path:
            data = {k: v for k, v in param.__dict__.items() if not k.startswith("__") and not callable(v) and not isinstance(v, type(param))}
            del data['boundary']
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            
    def load_single_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("All files", "*.*")],
            title="Open a file"
        )

        if file_path:
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
            param.__dict__.update(data)
            self.update_UI()


root = tk.Tk()
app = GUI(root)
root.mainloop()
