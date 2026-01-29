import json
import os
import subprocess
import time


map_size = 25
running_game = True

def git_push(filename,hint):
    # -q macht git leise, stdout/stderr=DEVNULL schluckt den Rest
    subprocess.run(["git", "add", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-q", "-m", f"Update {filename}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "push", "-q"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(hint)
    


def git_pull():
    subprocess.run(["git", "pull", "-q"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def show_board(view_list):
    """Zeigt das 5x5 Feld schick an."""
    icons = {0: "🌊", 2: "💦", 3: "💥"}
    print("\nGegnerisches Feld:")
    for i in range(0, 25, 5):
        row = view_list[i:i+5]
        print(" ".join([icons.get(x, "?") for x in row]))
    print()

def clear_terminal():
    # 'nt' steht für Windows (cmd/powershell), sonst 'clear' für Linux/Mac
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*30)
    print(f"   BATTLESHIPS ONLINE - {player_id.upper()}")
    print("="*30)








# --- Hauptprogramm ---

## Nur einmal beim Spiel start
#Namensabfrage
while True:
    player_id = input("Bist du p1 oder p2? ").lower()
    if player_id == "p1" or player_id == "p2":
        break
    else:
        print("Ungültige ID")

# Game Loop
while running_game:
    git_pull()
    clear_terminal()
    
    with open("game_state.json", "r") as f:
        state = json.load(f)
    
    if state["is_running"]:

        # 1. Prüfen ob ich dran bin
        if state["turn"] == player_id:

            current_map = state[f"{player_id}_view"]
            
            print(f"\n--- DEIN ZUG ({player_id}) ---")
            show_board(current_map)
            print(f"Letztes Ereignis: {state['last_move_result']}")
            

            while True:
                ziel = int(input("Wo schießt du hin (0-24)? "))
                if ziel<0 or ziel > map_size-1:
                    print("Kein gültiges Feld")
                elif current_map[ziel] == 2:
                    print("Dieses Feld hast du bereits beschossen")
                elif current_map[ziel] == 3:
                    print("Auf diesem Feld hast du bereits getroffen")
                else: break
            

            # move.json erstellen
            move = {"player": player_id, "coord": ziel}
            with open("move.json", "w") as f:
                json.dump(move, f)
                
            git_push("move.json","🚀 Zug abgeschickt! Warte auf Schiedsrichter...")
            print("Warte auf Schiedsrichter-Update (ca. 20-30 Sek)...")
            time.sleep(30) # Pause, damit GitHub Zeit zum Rechnen hat
        else:
            print("Gegner ist noch am Zug... Warte 10 Sek.")
            time.sleep(10)
    
    else:
        if state["winner"] != "":
            print(state["winner"])
            if str(state["winner"]) == player_id:
                print("Glückwunsch! Du hast gewonnen")
            else:
                print("Du hast leider verloren")
            
            time.sleep(5)
            while True:
                answer = str(input("Willst du noch eine Runde spielen?: Ja, Nein ").lower)
                if answer == "nein":
                    running_game = False
                    break
            

        if not state[f"{player_id}_placed"]:
            choosen_fields = []
            for i in range(1,4):
                while True:
                    field = int(input(f"Platziere Schiff Nr. {i}: "))
                    if field in choosen_fields:
                        print("Diese Feld hast du bereits gewählt")
                    elif field < 0 or field >= map_size:
                        print("Ungültiges Feld")           
                    else:
                        choosen_fields.append(field)
                        break
            
            lineup = [0] * 25 # Erzeugt eine Liste mit 25 Nullen
            for point in choosen_fields:
                lineup[point] = 1


            setup = {"player": player_id, "ships": lineup}
            with open(f"{player_id}_setup.json", "w") as f:
                json.dump(setup, f)
            git_push(f"{player_id}_setup.json","🚀 Aufstellung abgeschickt! Warte auf Schiedsrichter...")
            