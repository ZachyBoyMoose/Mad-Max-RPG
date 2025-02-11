import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json


class DnDBattleTrackerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("D&D Battle Tracker")

        self.initiative_order = []
        self.current_turn_index = 0
        self.combat_log = []

        self.setup_ui()
        self.create_log_window()

    def setup_ui(self):
        # Initiative Order Frame
        self.initiative_frame = ttk.Frame(self.root)
        self.initiative_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initiative List
        self.initiative_list = tk.Listbox(self.initiative_frame, height=20, width=50)
        self.initiative_list.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Initiative Buttons
        self.initiative_buttons = ttk.Frame(self.initiative_frame)
        self.initiative_buttons.pack(side="right", fill="y", padx=10, pady=10)

        ttk.Button(self.initiative_buttons, text="Add Combatant", command=self.add_combatant).pack(pady=5)
        ttk.Button(self.initiative_buttons, text="Add Multiple", command=self.add_multiple_combatants).pack(pady=5)
        ttk.Button(self.initiative_buttons, text="Next Turn", command=self.next_turn).pack(pady=5)
        ttk.Button(self.initiative_buttons, text="Adjust HP", command=self.adjust_hp).pack(pady=5)
        ttk.Button(self.initiative_buttons, text="Adjust Vehicle HP", command=self.adjust_vehicle_hp).pack(pady=5)
        ttk.Button(self.initiative_buttons, text="Add Status Effect", command=self.add_status).pack(pady=5)
        ttk.Button(self.initiative_buttons, text="Save State", command=self.save_state).pack(pady=5)
        ttk.Button(self.initiative_buttons, text="Load State", command=self.load_state).pack(pady=5)

    def create_log_window(self):
        self.log_window = tk.Toplevel(self.root)
        self.log_window.title("Combat Log")
        self.log_text = tk.Text(self.log_window, wrap="word", state="disabled", height=20, width=70)
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

    def log_action(self, action):
        self.combat_log.append(action)
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, action + "\n")
        self.log_text.configure(state="disabled")

    def add_combatant(self):
        name = self.simple_input("Enter combatant name:")
        if not name:
            return
        initiative_choice = messagebox.askyesno("Initiative Roll", "Roll initiative automatically?")
        if initiative_choice:
            initiative_modifier = int(self.simple_input("Enter initiative modifier:") or 0)
            initiative = random.randint(1, 20) + initiative_modifier
        else:
            initiative = int(self.simple_input("Enter initiative value:") or 0)

        hp = int(self.simple_input("Enter HP:") or 0)
        ac = int(self.simple_input("Enter AC:") or 0)

        has_vehicle = messagebox.askyesno("Vehicle", "Does this combatant have a vehicle?")
        vehicle = None
        if has_vehicle:
            vehicle_name = self.simple_input("Enter vehicle name:")
            vehicle_hp = int(self.simple_input("Enter vehicle HP:") or 0)
            vehicle_ac = int(self.simple_input("Enter vehicle AC:") or 0)
            vehicle = {"name": vehicle_name, "hp": vehicle_hp, "ac": vehicle_ac}

        self.initiative_order.append({
            "name": name,
            "initiative": initiative,
            "hp": hp,
            "ac": ac,
            "vehicle": vehicle,
            "status_effects": []
        })
        self.log_action(f"Added combatant {name} with initiative {initiative}.")
        self.sort_initiative()
        self.update_initiative_list()

    def add_multiple_combatants(self):
        base_name = self.simple_input("Enter base name for NPCs:")
        if not base_name:
            return
        count = int(self.simple_input("Enter number of NPCs:") or 0)
        initiative_modifier = int(self.simple_input("Enter initiative modifier:") or 0)
        hp = int(self.simple_input("Enter HP for each NPC:") or 0)
        ac = int(self.simple_input("Enter AC for each NPC:") or 0)

        has_vehicle = messagebox.askyesno("Vehicle", "Do these NPCs have vehicles?")
        vehicle_name = None
        vehicle_hp = 0
        vehicle_ac = 0

        if has_vehicle:
            vehicle_name = self.simple_input("Enter vehicle name:")
            vehicle_hp = int(self.simple_input("Enter vehicle HP:") or 0)
            vehicle_ac = int(self.simple_input("Enter vehicle AC:") or 0)

        for i in range(1, count + 1):
            initiative = random.randint(1, 20) + initiative_modifier
            vehicle = None
            if has_vehicle:
                vehicle = {"name": vehicle_name, "hp": vehicle_hp, "ac": vehicle_ac}

            self.initiative_order.append({
                "name": f"{base_name} {i}",
                "initiative": initiative,
                "hp": hp,
                "ac": ac,
                "vehicle": vehicle,
                "status_effects": []
            })
        self.log_action(f"Added {count} NPCs with base name {base_name}.")
        self.sort_initiative()
        self.update_initiative_list()

    def next_turn(self):
        if not self.initiative_order:
            messagebox.showinfo("Info", "No combatants in the initiative order.")
            return
        self.current_turn_index = (self.current_turn_index + 1) % len(self.initiative_order)
        current_combatant = self.initiative_order[self.current_turn_index]
        self.log_action(f"It is now {current_combatant['name']}'s turn.")
        self.update_initiative_list()

    def adjust_hp(self):
        selected_index = self.initiative_list.curselection()
        if not selected_index:
            return
        idx = selected_index[0]
        combatant = self.initiative_order[idx]
        amount = int(self.simple_input(f"Adjust HP for {combatant['name']}:") or 0)
        combatant["hp"] += amount
        self.log_action(f"{combatant['name']}'s HP adjusted by {amount}. New HP: {combatant['hp']}.")
        self.update_initiative_list()

    def adjust_vehicle_hp(self):
        selected_index = self.initiative_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No combatant selected.")
            return
        idx = selected_index[0]
        combatant = self.initiative_order[idx]
        if not combatant["vehicle"]:
            messagebox.showerror("Error", f"{combatant['name']} has no vehicle.")
            return
        amount = int(self.simple_input(f"Adjust vehicle HP for {combatant['name']}:") or 0)
        combatant["vehicle"]["hp"] += amount
        self.log_action(f"{combatant['name']}'s vehicle HP adjusted by {amount}. New HP: {combatant['vehicle']['hp']}.")
        self.update_initiative_list()

    def add_status(self):
        selected_index = self.initiative_list.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No combatant selected.")
            return
        idx = selected_index[0]
        combatant = self.initiative_order[idx]
        status = self.simple_input(f"Enter status effect for {combatant['name']}:")
        if not status:
            return
        combatant["status_effects"].append(status)
        self.log_action(f"Added status effect '{status}' to {combatant['name']}.")
        self.update_initiative_list()

    def save_state(self):
        file_path = simpledialog.askstring("Save State", "Enter the file name to save:")
        if not file_path:
            return
        data = {
        "initiative_order": self.initiative_order,
        "current_turn_index": self.current_turn_index,
        "combat_log": self.combat_log
        }
        try:
            with open(f"{file_path}.json", "w") as file:
                json.dump(data, file, indent=4)
            self.log_action(f"State saved to {file_path}.json.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save state: {e}")

    def load_state(self):
        file_path = simpledialog.askstring("Load State", "Enter the file name to load:")
        if not file_path:
            return
        try:
            with open(f"{file_path}.json", "r") as file:
                data = json.load(file)
            self.initiative_order = data.get("initiative_order", [])
            self.current_turn_index = data.get("current_turn_index", 0)
            self.combat_log = data.get("combat_log", [])

            # Update the UI components
            self.update_initiative_list()
            self.log_text.configure(state="normal")
            self.log_text.delete(1.0, tk.END)
            for action in self.combat_log:
                self.log_text.insert(tk.END, action + "\n")
            self.log_text.configure(state="disabled")

            self.log_action(f"State loaded from {file_path}.json.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File {file_path}.json not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load state: {e}")

    def simple_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

    def sort_initiative(self):
        self.initiative_order.sort(key=lambda c: c["initiative"], reverse=True)

    def update_initiative_list(self):
        self.initiative_list.delete(0, tk.END)
        for idx, combatant in enumerate(self.initiative_order):
            entry = f"{combatant['name']} (Init: {combatant['initiative']}, HP: {combatant['hp']}, AC: {combatant['ac']})"
            if combatant["vehicle"]:
                entry += f" [Vehicle: {combatant['vehicle']['name']}, HP: {combatant['vehicle']['hp']}, AC: {combatant['vehicle']['ac']}]"
            self.initiative_list.insert(tk.END, entry)
            if idx == self.current_turn_index:
                self.initiative_list.itemconfig(tk.END, {'bg': 'lightblue'})


if __name__ == "__main__":
    root = tk.Tk()
    app = DnDBattleTrackerUI(root)
    root.mainloop()
