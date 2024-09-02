import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

import dungeon_maker
import map_to_image
import map_to_json
import parameter as param
import tile_crop

map_type_dispaly = ["Dungeon", "Cave", "Plain", "Field"]
map_type_value = [0, 1, 2, 3]
output_path = 'output/'

def validate_range(value, min_value, max_value):
    try:
        if min_value <= int(value) <= max_value:
            return True
        else:
            return False
    except ValueError:
        return False

class ParameterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Parameter UI")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        # Left Side
        sidebar = tk.Frame(root, padx=10, pady=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar, text="Parameters", font=("Arial", 16)).pack(pady=(0, 10))

        tk.Label(sidebar, text="Map Type").pack(anchor=tk.W)
        self.map_type = tk.StringVar()
        map_type_menu = ttk.Combobox(sidebar, textvariable=self.map_type, values=map_type_dispaly, state="readonly")
        map_type_menu.set(map_type_dispaly[0])
        map_type_menu.pack()

        self.map_width = self.create_number_field(sidebar, "Map Width", 10, 300, 48)
        self.map_height = self.create_number_field(sidebar, "Map Height", 10, 300, 48)
        self.map_padding = self.create_slider(sidebar, "Map Padding", 0, 9, 4)
        self.wall_height = self.create_slider(sidebar, "Wall Height", 1, 9, 2)

        # self.create_range_field(sidebar, "Room Min Size", 0, 100, 25)
        self.room_padding = self.create_slider(sidebar, "Room Padding", 0, 100, 0, False)
        self.corridor_wide_auto = self.create_switch(sidebar, "Auto Corridor Wide", False)
        self.corridor_wide = self.create_slider(sidebar, "Corridor Wide", 0, 100, 50, False)
        self.room_padding = self.create_slider(sidebar, "Room Frequency", 0, 100, 50, False)

        tk.Button(sidebar, text="Generate", command=self.on_submit).pack(pady=(10, 0))

        # Center
        self.main_content = tk.Frame(root, padx=10, pady=10)
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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

    def create_switch(self, parent, label, default_val):
        frame = tk.Frame(parent)
        frame.pack(pady=(15, 0))
        tk.Label(frame, text=label).pack(anchor=tk.W)
        switch = tk.BooleanVar(value=default_val)
        checkbutton = tk.Checkbutton(frame, variable=switch)
        checkbutton.pack()
        return switch

    def update_image(self, img_path):
        width = self.result_image.winfo_width()
        height = self.result_image.winfo_height()

        image = Image.open(img_path).resize((width, height))
        photo = ImageTk.PhotoImage(image)

        self.result_image.config(image=photo)
        self.result_image.image = photo  # Keep a reference to avoid garbage collection

    def on_submit(self):
        def setParam(key, value):
            if hasattr(param, key):
                setattr(param, key, int(value))
                
        def mappedValue(v, a, b):
            return int(a + (v / 100) * (b - a));
        
        if(not validate_range(self.map_width.get(), 10, 300)):
            return
        if(not validate_range(self.map_height.get(), 10, 300)):
            return

        self.result_image.text = "Generating..."
        map_type_map = dict(zip(map_type_dispaly, map_type_value))

        setParam('map_type', map_type_map[self.map_type.get()])
        setParam('map_width', int(self.map_width.get()))
        setParam('map_height', int(self.map_height.get()))
        setParam('map_padding', self.map_padding.get())
        setParam('wall_height', self.wall_height.get())
        
        # setParam('room_min_size', mappedValue(self.room_min_size.get(), 4, min(self.map_width.get(), self.map_height.get()) - self.map_padding.get()))
        # setParam('room_max_size', mappedValue(self.room_max_size.get(), 4, min(self.map_width.get(), self.map_height.get()) - self.map_padding.get()))
        setParam('room_padding', mappedValue(self.room_padding.get(), 0, self.room_min_size.get() // 2))
        setParam('corridor_wide_auto', self.corridor_wide_auto.get())
        setParam('corridor_wide', mappedValue(self.corridor_wide.get(), 1, (self.room_min_size.get() - self.wall_height.get()) // 2))
        setParam('room_freq', self.room_freq.get())

        tileset = tile_crop.main()
        dungeon = dungeon_maker.main()
        img_path = map_to_image.main(dungeon.map, tileset, param.map_id, output_path)
        map_to_json.main(dungeon.map, param.tileset_id, param.map_id, output_path)

        self.update_image(img_path)


# Create and run the Tkinter application     
root = tk.Tk()
app = ParameterApp(root)
root.mainloop()
