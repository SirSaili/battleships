import json
import os




def run_game():
    def clear_game():
        state["last_move_result"] = "Game Over"
        state["is_running"] = False
        state["p1_placed"] = ""
        state["p2_placed"] = ""
        
    # 1. Dateien laden
    with open("game_state.json", "r") as f:
        state = json.load(f)

    is_running = state["is_running"]

    if is_running:

        if not os.path.exists("move.json"):
            print("Kein Spielzug vorhanden.")
            return
        
        with open("move.json", "r") as f:
            move = json.load(f)
    
        player = move["player"]  # "p1" oder "p2"
        coord = move["coord"]    # 0 bis 24
    
        # 2. Prüfen, wer dran ist
        if player != state["turn"]:
            state["last_move_result"] = f"Falscher Spieler! {state['turn']} ist dran."
        else:
            # 3. Logik: Treffer oder Wasser?
            # Wenn p1 schießt, gucken wir bei p2_ships nach
            target_ships = "p2_ships" if player == "p1" else "p1_ships"
            player_view = "p1_view" if player == "p1" else "p2_view"
    
            if state[target_ships][coord] == 1:
                state[player_view][coord] = 3 # Treffer
                state["last_move_result"] = f"{player} hat getroffen auf Feld {coord}!"
            else:
                state[player_view][coord] = 2 # Wasser
                state["last_move_result"] = f"{player} hat verfehlt auf Feld {coord}."
    
            # Spieler wechseln
            state["turn"] = "p2" if player == "p1" else "p1"
    
        

        # Hat jemand gewonnen
        if state["p1_view"].count(3) == 3:
            state["winner"] = "p1"
        
        elif state["p2_view"].count(3) == 3:
            state["winner"] = "p2"


        # 4. Speichern und aufräumen
        with open("game_state.json", "w") as f:
            json.dump(state, f, indent=4)
        
        os.remove("move.json") # Spielzug löschen, damit er nicht doppelt zählt
    else:
        p1_placed = state["p1_placed"]
        p2_placed = state["p2_placed"]
        p1_ships = []
        p2_ships = []

        if not p1_placed:
            if not os.path.exists("p1_setup.json"):
                print("Keine Aufstellung von p1 vorhanden.")
                return
            
            with open("p1_setup.json", "r") as f:
                p1_setup = json.load(f)
            state["p1_ships"] = p1_setup["ships"]
            state["p1_placed"] = True
            os.remove("p1_setup.json")


        if not p2_placed:
            if not os.path.exists("p2_setup.json"):
                print("Keine Aufstellung von p2 vorhanden.")
                return
            
            with open("p2_setup.json", "r") as f:
                p2_setup = json.load(f)
            state["p2_ships"] = p2_setup["ships"]
            state["p2_placed"] = True
            os.remove("p2_setup.json")
        

        if state["p1_placed"] and state["p2_placed"]:
            state["is_running"] = True
            
        with open("game_state.json", "w") as f:
            json.dump(state, f, indent=4)

        
if __name__ == "__main__":
    run_game()
