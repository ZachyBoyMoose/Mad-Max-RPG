import tkinter as tk
from tkinter import messagebox, scrolledtext

# Data storage
characters = {}
vehicles = {}

# Function to add an NPC
def add_npc():
    def save_npc():
        name = name_entry.get()
        stats = {
            "AC": ac_entry.get(),
            "HP": hp_entry.get(),
            "Speed": speed_entry.get(),
            "Weapons": weapons_entry.get(),
            "Abilities": abilities_entry.get()
        }
        characters[name] = stats
        messagebox.showinfo("Success", f"{name} has been added to the NPC list!")
        add_window.destroy()
        refresh_display()

    add_window = tk.Toplevel(root)
    add_window.title("Add NPC")
    add_window.geometry("300x250")

    tk.Label(add_window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1)

    tk.Label(add_window, text="AC:").grid(row=1, column=0)
    ac_entry = tk.Entry(add_window)
    ac_entry.grid(row=1, column=1)

    tk.Label(add_window, text="HP:").grid(row=2, column=0)
    hp_entry = tk.Entry(add_window)
    hp_entry.grid(row=2, column=1)

    tk.Label(add_window, text="Speed:").grid(row=3, column=0)
    speed_entry = tk.Entry(add_window)
    speed_entry.grid(row=3, column=1)

    tk.Label(add_window, text="Weapons:").grid(row=4, column=0)
    weapons_entry = tk.Entry(add_window)
    weapons_entry.grid(row=4, column=1)

    tk.Label(add_window, text="Abilities:").grid(row=5, column=0)
    abilities_entry = tk.Entry(add_window)
    abilities_entry.grid(row=5, column=1)

    tk.Button(add_window, text="Save", command=save_npc).grid(row=6, column=0, columnspan=2)

# Function to add a vehicle
def add_vehicle():
    def save_vehicle():
        name = name_entry.get()
        stats = {
            "AC": ac_entry.get(),
            "HP": hp_entry.get(),
            "Speed": speed_entry.get(),
            "Weapons": weapons_entry.get(),
            "Abilities": abilities_entry.get()
        }
        vehicles[name] = stats
        messagebox.showinfo("Success", f"{name} has been added to the vehicle list!")
        add_window.destroy()
        refresh_display()

    add_window = tk.Toplevel(root)
    add_window.title("Add Vehicle")
    add_window.geometry("300x250")

    tk.Label(add_window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1)

    tk.Label(add_window, text="AC:").grid(row=1, column=0)
    ac_entry = tk.Entry(add_window)
    ac_entry.grid(row=1, column=1)

    tk.Label(add_window, text="HP:").grid(row=2, column=0)
    hp_entry = tk.Entry(add_window)
    hp_entry.grid(row=2, column=1)

    tk.Label(add_window, text="Speed:").grid(row=3, column=0)
    speed_entry = tk.Entry(add_window)
    speed_entry.grid(row=3, column=1)

    tk.Label(add_window, text="Weapons:").grid(row=4, column=0)
    weapons_entry = tk.Entry(add_window)
    weapons_entry.grid(row=4, column=1)

    tk.Label(add_window, text="Abilities:").grid(row=5, column=0)
    abilities_entry = tk.Entry(add_window)
    abilities_entry.grid(row=5, column=1)

    tk.Button(add_window, text="Save", command=save_vehicle).grid(row=6, column=0, columnspan=2)

# Function to refresh the display
def refresh_display():
    display_area.delete(1.0, tk.END)
    display_area.insert(tk.END, "=== NPCs ===\n")
    for name, stats in characters.items():
        display_area.insert(tk.END, f"{name}:\n")
        for stat, value in stats.items():
            display_area.insert(tk.END, f"  {stat}: {value}\n")
        display_area.insert(tk.END, "\n")

    display_area.insert(tk.END, "=== Vehicles ===\n")
    for name, stats in vehicles.items():
        display_area.insert(tk.END, f"{name}:\n")
        for stat, value in stats.items():
            display_area.insert(tk.END, f"  {stat}: {value}\n")
        display_area.insert(tk.END, "\n")

# Main window
root = tk.Tk()
root.title("Wasteland Tracker")
root.geometry("600x400")

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add NPC", command=add_npc).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Add Vehicle", command=add_vehicle).grid(row=0, column=1, padx=5)

# Display area
display_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
display_area.pack(padx=10, pady=10)

# Initial display refresh
refresh_display()

# Run the program
root.mainloop()
