import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import math


class MadMaxMapManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Mad Max RPG Map Manager")

        # Canvas for the map
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Units and map data
        self.units = []  # Stores all units
        self.obstacles = []  # Stores obstacles
        self.shapes = []  # Stores shapes
        self.map_size = (100, 100)  # Default map size in feet
        self.grid_size = 10  # Default grid square size
        self.background_color = "lightgray"  # Default background color
        self.measure_line = None  # Line for measuring distance
        self.start_x, self.start_y = None, None  # Start point for measurement
        self.selected_unit = None  # Currently selected unit
        self.current_symbol = None  # Current symbol for units

        # Symbols
        self.player_symbols = {
            "💥": "Explosion",
            "💉": "Syringe",
            "📖": "Book",
            "🎸": "Guitar",
            "🔧": "Wrench",
            "🐺": "Wolf",
        }
        self.npc_symbols = ["😊", "💀"]  # Happy face, Skull
        self.vehicle_symbols = ["🏍️", "🚗", "🚛"]  # Motorcycle, Car, Semi-truck

        # Controls
        control_frame = tk.Frame(root)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        button_texts = [
            ("Generate Map", self.generate_map),
            ("Add Random Players", lambda: self.show_symbol_buttons("Player")),
            ("Add Random NPCs", lambda: self.show_symbol_buttons("NPC")),
            ("Add Random Vehicles", lambda: self.show_symbol_buttons("Vehicle")),
            ("Add Random Items", lambda: self.add_random_units("Item")),
            ("Edit Name", self.edit_name),
            ("Delete Unit", self.delete_unit),
            ("Measure Distance", self.measure_distance_mode),
            ("Create Shape", self.create_shape_mode)
        ]

        for i, (text, command) in enumerate(button_texts):
            row = i // 4
            col = i % 4
            tk.Button(control_frame, text=text, command=command).grid(row=row, column=col, pady=5, padx=5)

        # Distance measurement display
        self.distance_label = tk.Label(control_frame, text="Measured Distance: N/A")
        self.distance_label.grid(row=len(button_texts) // 4 + 1, column=0, columnspan=4, pady=10)

        # Symbol selection frame (hidden initially)
        self.symbol_frame = tk.Frame(root)
        self.symbol_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.symbol_frame.pack_forget()

        # Canvas bindings
        self.canvas.bind("<Button-1>", self.select_unit)
        self.canvas.bind("<B1-Motion>", self.drag_unit)
        self.canvas.bind("<ButtonRelease-1>", self.clear_measurement)

    def show_symbol_buttons(self, unit_type):
        """Show buttons for symbol selection based on unit type."""
        self.symbol_frame.pack(fill=tk.Y)
        for widget in self.symbol_frame.winfo_children():
            widget.destroy()

        tk.Label(self.symbol_frame, text=f"Select {unit_type} Symbol:").pack(pady=5)

        if unit_type == "Player":
            symbols = self.player_symbols
        elif unit_type == "NPC":
            symbols = self.npc_symbols
        elif unit_type == "Vehicle":
            symbols = self.vehicle_symbols
        else:
            symbols = []

        for symbol in symbols:
            tk.Button(self.symbol_frame, text=symbol, command=lambda s=symbol: self.set_symbol_and_add(unit_type, s)).pack(pady=2)

    def set_symbol_and_add(self, unit_type, symbol):
        """Set the symbol and add random units."""
        self.current_symbol = symbol
        self.add_random_units(unit_type)
        self.symbol_frame.pack_forget()

    def generate_map(self):
        """Generate a new map with the selected location and background color."""
        self.canvas.delete("all")
        self.units = []
        self.obstacles = []
        self.shapes = []

        # Set background color
        colors = {
            "Rust": "#8B4513",
            "Dust": "#D2B48C",
            "Sand": "#F4A460",
            "Blood Red": "#8B0000",
            "Chrome": "#C0C0C0",
            "Black": "#000000",
        }
        self.background_color = colors.get("Dust", "lightgray")
        self.canvas.config(bg=self.background_color)

        # Adjust map size and grid size
        self.map_size = (100, 100)  # Default 100x100 feet
        self.grid_size = 800 // self.map_size[0]

        # Draw the grid
        self.draw_grid()

    def draw_grid(self):
        """Draw the grid on the map."""
        for i in range(0, 800, self.grid_size):
            self.canvas.create_line(i, 0, i, 600, fill="lightgray")
        for j in range(0, 600, self.grid_size):
            self.canvas.create_line(0, j, 800, j, fill="lightgray")

    def measure_distance_mode(self):
        """Enable distance measurement mode."""
        self.canvas.bind("<Button-1>", self.start_measurement)
        self.canvas.bind("<B1-Motion>", self.update_measurement)
        self.canvas.bind("<ButtonRelease-1>", self.clear_measurement)

    def start_measurement(self, event):
        """Start measuring distance."""
        self.start_x, self.start_y = event.x, event.y
        self.measure_line = self.canvas.create_line(event.x, event.y, event.x, event.y, fill="red", dash=(4, 2))

    def update_measurement(self, event):
        """Update the measurement line."""
        if self.measure_line:
            self.canvas.coords(self.measure_line, self.start_x, self.start_y, event.x, event.y)
            distance = math.sqrt((event.x - self.start_x)**2 + (event.y - self.start_y)**2)
            feet_distance = (distance / 800) * self.map_size[0]  # Convert pixels to feet
            self.distance_label.config(text=f"Measured Distance: {feet_distance:.2f} ft")

    def clear_measurement(self, event=None):
        """Clear the measurement line."""
        if self.measure_line:
            self.canvas.delete(self.measure_line)
            self.measure_line = None
            self.distance_label.config(text="Measured Distance: N/A")

        # Restore unit selection bindings
        self.canvas.bind("<Button-1>", self.select_unit)
        self.canvas.bind("<B1-Motion>", self.drag_unit)

    def create_shape_mode(self):
        """Enable shape creation mode."""
        self.canvas.bind("<Button-1>", self.start_shape)
        self.canvas.bind("<B1-Motion>", self.resize_shape)
        self.canvas.bind("<ButtonRelease-1>", self.finalize_shape)

    def start_shape(self, event):
        """Start creating a shape."""
        self.start_x, self.start_y = event.x, event.y
        self.current_shape = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline="black", width=2)

    def resize_shape(self, event):
        """Resize the current shape."""
        self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)

    def finalize_shape(self, event):
        """Finalize the shape."""
        self.shapes.append(self.current_shape)
        self.start_x, self.start_y = None, None
        self.current_shape = None

    def add_random_units(self, unit_type):
        """Add random units of a specific type."""
        count = simpledialog.askinteger("Random Units", f"Number of {unit_type}s to add:", minvalue=0, maxvalue=50)
        if not count:
            return

        for i in range(count):
            x, y = random.randint(20, 780), random.randint(20, 580)
            symbol = self.current_symbol or "?"  # Fallback in case symbol isn't set
            self.add_unit_to_canvas(unit_type, f"{unit_type} #{i+1}", x, y, symbol)

    def add_unit_to_canvas(self, unit_type, name, x, y, symbol):
        """Add a unit to the canvas."""
        color = {"Player": "green", "NPC": "red", "Vehicle": "blue", "Item": "yellow"}.get(unit_type, "black")
        unit = self.canvas.create_text(x, y, text=symbol, fill=color, font=("Helvetica", 16), tags="unit")
        self.units.append({"id": unit, "type": unit_type, "name": name, "x": x, "y": y})

    def delete_unit(self):
        """Delete the selected unit."""
        if not self.selected_unit:
            messagebox.showerror("Error", "No unit selected!")
            return

        self.canvas.delete(self.selected_unit)
        self.units = [u for u in self.units if u["id"] != self.selected_unit]
        self.selected_unit = None
        symbol()
        """Add a unit to the canvas."""
        color = {"Player": "green", "NPC": "red", "Vehicle": "blue", "Item": "yellow"}.get(unit_type, "black")
        unit = self.canvas.create_text(x, y, text=symbol, fill=color, font=("Helvetica", 16), tags="unit")
        self.units.append({"id": unit, "type": unit_type, "name": name, "x": x, "y": y})
        return unit

    def delete_unit(self):
        """Delete the selected unit."""
        if not self.selected_unit:
            messagebox.showerror("Error", "No unit selected!")
            return

        self.canvas.delete(self.selected_unit)
        self.units = [u for u in self.units if u["id"] != self.selected_unit]
        self.selected_unit = None

    def edit_name(self):
        """Edit the name of a selected unit."""
        if not self.selected_unit:
            messagebox.showerror("Error", "No unit selected!")
            return

        new_name = simpledialog.askstring("Edit Name", "Enter new name:")
        if new_name:
            for unit in self.units:
                if unit["id"] == self.selected_unit:
                    unit["name"] = new_name
                    break
            self.canvas.itemconfig(self.selected_unit, text=f"{new_name}\n{self.canvas.itemcget(self.selected_unit, 'text')}")

    def select_unit(self, event):
        """Select a unit on the map."""
        clicked_item = self.canvas.find_withtag("current")
        if clicked_item:
            self.selected_unit = clicked_item[0]

    def drag_unit(self, event):
        """Drag a selected unit."""
        if self.selected_unit:
            self.canvas.coords(self.selected_unit, event.x, event.y)
            for unit in self.units:
                if unit["id"] == self.selected_unit:
                    unit["x"], unit["y"] = event.x, event.y

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = MadMaxMapManager(root)
    root.mainloop()

   

