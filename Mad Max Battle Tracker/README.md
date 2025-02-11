# Mad-Max-RPG-Battle-Tracker
For managing initiative order for a DnD style RPG that includes vehicles

Key Features:

Initiative Order Management:

Tracks the initiative order of combatants, sorted by their initiative rolls.

Highlights the current combatant's turn.

Combatant Management:

Add individual combatants with custom names, initiative rolls, HP, and AC.

Add multiple NPCs (Non-Player Characters) at once with shared stats.

Supports vehicles for combatants, including vehicle HP and AC.

Combat Actions:

Move to the next combatant's turn.

Adjust HP for combatants and their vehicles.

Add status effects (e.g., poisoned, stunned) to combatants.

Combat Log:

Logs all actions (e.g., adding combatants, adjusting HP, changing turns) in a separate window for reference.

Save and Load State:

Save the current state (initiative order, combat log, etc.) to a JSON file.

Load a previously saved state from a JSON file.

User-Friendly Interface:

Uses tkinter for a simple GUI with buttons, input dialogs, and a listbox to display the initiative order.

How It Works:
The application initializes with a main window containing the initiative order and buttons for actions like adding combatants, adjusting HP, and moving to the next turn.

A separate log window displays the combat log.

Combatants are stored as dictionaries in a list (initiative_order), and their stats are displayed in a listbox.

The application uses JSON to save and load the state of the battle, including combatant details and the combat log.
