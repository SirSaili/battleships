import json
import os

# 1. Spielstand laden (oder neu erstellen)
file_path = "game_state.json"
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        game_state = json.load(f)
else:
    game_state = {"hits": 0, "status": "Start"}

# 2. Die "Logik" ausführen
game_state["hits"] += 1
game_state["status"] = "Update durch Python"

# 3. Speichern
with open(file_path, "w") as f:
    json.dump(game_state, f, indent=4)

print(f"Logik ausgeführt. Treffer jetzt bei: {game_state['hits']}")
