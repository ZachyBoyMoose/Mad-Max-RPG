import random
import tkinter as tk
from tkinter import messagebox

# Items by level
items = {
    1: {
        "Weapons": [
            {"name": "Rusty Shiv", "damage": "1d4 piercing", "special": "Advantage on attack rolls from stealth."},
            {"name": "Scrap Hammer", "damage": "1d6 bludgeoning", "special": "Knocks enemy prone on a critical hit."},
            {"name": "Makeshift Slingshot", "damage": "1d6 bludgeoning", "special": "Extra 1 damage with jagged scrap."},
            {"name": "Bent Crowbar", "damage": "1d6 bludgeoning", "special": "Advantage on Strength checks to pry."},
            {"name": "Jagged Glass Shiv", "damage": "1d4 slashing", "special": "Causes bleed on critical hit (1 damage per turn)."}
        ],
        "Armor": [
            {"name": "Padded Leather Jacket", "ac_bonus": "+1 AC", "special": "Resistance to slashing damage."},
            {"name": "Scrap Bracers", "ac_bonus": "+1 AC", "special": "Reduces ranged damage by 1."},
            {"name": "Rusty Pauldron", "ac_bonus": "+1 AC", "special": "+1 to Intimidation checks."}
        ],
        "Vehicle Parts": [
            {"name": "Rusted Tires", "effect": "Standard tires", "special": "25% chance of blowout in chases."},
            {"name": "Leaky Fuel Tank", "effect": "Holds 3 extra gallons", "special": "10% chance to spill fuel."}
        ],
        "Consumables": [
            {"name": "Tin of Mystery Paste", "effect": "Restores 1d6 HP", "special": "Roll a d20; on 1-5, causes nausea."},
            {"name": "Leaky Canteen", "effect": "Restores 1d4 HP", "special": "Provides half a unit of water."}
        ]
    },
    2: {
        "Weapons": [
            {"name": "Spiked Baseball Bat", "damage": "1d8 bludgeoning + 1 piercing", "special": "Advantage on Intimidation checks."},
            {"name": "Bladed Chain Whip", "damage": "1d8 slashing", "special": "Trips target on critical hit (DC 13)."},
            {"name": "Exploding Throwing Knives", "damage": "1d6 piercing + 1d6 fire", "special": "Single-use, 10 ft. radius explosion."},
            {"name": "Flintlock Hand Cannon", "damage": "1d10 piercing", "special": "Reload required after every shot."}
        ],
        "Armor": [
            {"name": "Patchwork Leather Pants", "ac_bonus": "+1 AC", "special": "Resistance to slashing damage."},
            {"name": "Scrap Helmet with Goggles", "ac_bonus": "+1 AC", "special": "Advantage against blinding effects."},
            {"name": "Duct Tape Chestplate", "ac_bonus": "+2 AC", "special": "Breaks after taking 25 damage."}
        ],
        "Vehicle Parts": [
            {"name": "Plated Doors", "effect": "+1 AC for the vehicle", "special": "Provides partial cover for passengers."},
            {"name": "Explosive Barrel Dispenser", "effect": "Drops barrels that explode (3d6 fire, 10 ft. radius)."},
            {"name": "Small Nitro Cannister", "effect": "+30 ft. speed for 1 round", "special": "Single-use."}
        ],
        "Consumables": [
            {"name": "Homemade Moonshine", "effect": "Restores 1d8 HP", "special": "+1 attack rolls for 1 minute but disadvantage on Wisdom saves."},
            {"name": "Rotten Meat Jerky", "effect": "Restores 2d4 HP", "special": "25% chance of food poisoning (1d4 poison damage)."},
            {"name": "Stim Canister", "effect": "Restores 1d8 HP", "special": "+2 temporary AC for 1 minute, then exhaustion sets in."}
        ]
    },
    3: {
        "Weapons": [
            {"name": "Sawblade Launcher", "damage": "2d6 slashing", "special": "Ricochets to one additional target."},
            {"name": "Harpoon Gun", "damage": "2d6 piercing", "special": "Grapples targets (escape DC 14)."},
            {"name": "Buzzsaw Blade", "damage": "1d8 slashing", "special": "Severs a limb on a critical hit (DC 15 Constitution save)."}
        ],
        "Armor": [
            {"name": "Chainmail Cloak", "ac_bonus": "+2 AC", "special": "Resistance to fire damage."},
            {"name": "Reinforced Visor Helmet", "ac_bonus": "+1 AC", "special": "Advantage on Perception checks involving sight."},
            {"name": "Hardened Scrap Boots", "ac_bonus": "+1 AC", "special": "Resistance to spike traps and caltrops."}
        ],
        "Vehicle Parts": [
            {"name": "Flaming Spikes", "effect": "+1d6 fire damage to ramming attacks."},
            {"name": "Reinforced Undercarriage", "effect": "Halves damage from terrain hazards like land mines."},
            {"name": "Spike Launchers", "effect": "Fires spikes in a 15 ft. cone", "special": "Deals 2d6 piercing damage."}
        ],
        "Consumables": [
            {"name": "Blood Stim", "effect": "Restores 2d8 HP", "special": "+10 ft. movement for 1 minute, 1d4 damage after."},
            {"name": "Molten Brew Flask", "effect": "Restores 1d6 HP", "special": "Grants advantage on Strength checks for 1 hour."}
        ]
    },
    4: {
        "Weapons": [
            {"name": "Fire Axe of Fury", "damage": "1d12 slashing", "special": "+1 attack rolls, ignites target on crit."},
            {"name": "Shrapnel Launcher", "damage": "3d6 piercing (cone)", "special": "15 ft. cone; DC 15 Dex save for half damage."},
            {"name": "Molotov Launcher", "damage": "3d6 fire (20 ft. radius)", "special": "Sets terrain ablaze for 2 rounds."}
        ],
        "Armor": [
            {"name": "Burned Wastelander Plate", "ac_bonus": "+4 AC", "special": "Immunity to fire damage for 1 round when struck."},
            {"name": "Spiked Cloak", "ac_bonus": "+2 AC", "special": "Deals 1d6 piercing damage to grappling enemies."},
            {"name": "Flameproof Overalls", "ac_bonus": "+1 AC", "special": "Resistance to fire damage."}
        ],
        "Vehicle Parts": [
            {"name": "Tread Spikes", "effect": "Deals 1d8 slashing damage to those disabling tires."},
            {"name": "Mounted Catapult", "effect": "Launches debris at range, dealing 3d8 bludgeoning damage."},
            {"name": "Reinforced Axles", "effect": "Reduces vehicle damage from rough terrain by half."}
        ]
    },
    5: {
        "Weapons": [
            {"name": "The Boomstick", "damage": "3d10 piercing", "special": "Knocks enemies back 15 ft. on a critical hit."},
            {"name": "Skull-Crusher Maul", "damage": "3d10 bludgeoning", "special": "Critical hit stuns target for 1 round (DC 15)."},
            {"name": "Doomsday Flamethrower", "damage": "4d8 fire (20 ft. cone)", "special": "Ignites the terrain for 1 minute."}
        ],
        "Armor": [
            {"name": "Chrome-Dipped Shield", "ac_bonus": "+3 AC", "special": "Blinds enemies within 10 ft. on crit block (DC 15)."},
            {"name": "Reinforced Exo-Suit", "ac_bonus": "+5 AC", "special": "+2 to Strength and Constitution checks."}
        ],
        "Vehicle Parts": [
            {"name": "Nitro Quad Boost", "effect": "+40 ft. speed for 3 rounds", "special": "Consumes 2 gallons per use."},
            {"name": "Iron Ram Front", "effect": "+2d10 bludgeoning damage to ramming attacks."},
            {"name": "Mounted Flamethrower", "effect": "4d6 fire (15 ft. cone)", "special": "Mounted use only."}
        ]
    }
    # You can add Levels 3, 4, and 5 here
}

# Generate a random item for the chosen level
def generate_item(level):
    if level not in items:
        messagebox.showerror("Error", "Invalid level selected.")
        return
    category = random.choice(list(items[level].keys()))
    item = random.choice(items[level][category])
    result = f"--- {category[:-1].upper()} FOUND! ---\n"
    for key, value in item.items():
        result += f"{key.capitalize()}: {value}\n"
    return result

# Button click event
def on_generate(level):
    result = generate_item(level)
    if result:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)

# Create GUI
root = tk.Tk()
root.title("Wasteland Random Item Generator")

# Title Label
title_label = tk.Label(root, text="Wasteland Random Item Generator", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Buttons for levels
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

for level in range(1, 6):  # Buttons for Levels 1 to 5
    tk.Button(
        button_frame, text=f"Generate Level {level} Item",
        command=lambda lvl=level: on_generate(lvl),
        width=20, height=2
    ).grid(row=0, column=level-1, padx=5)

# Output Textbox
output_text = tk.Text(root, wrap=tk.WORD, width=50, height=10, font=("Courier", 10))
output_text.pack(pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white", font=("Helvetica", 12, "bold"))
exit_button.pack(pady=10)

# Run the application
root.mainloop()
