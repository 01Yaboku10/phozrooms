"""Huvudmodul för huvudprogrammet av Phöz Rooms"""

import menu
import movement
import generation
import failsafe

def main() -> None:
    """Huvudprogrammet för Phöz Rooms"""
    rto = True
    while rto:
        main_menu = menu.Main_menu()
        game_map, mapsize, difficulty = main_menu.menu()  #  kör menyn och retunerar spelbanan och dess storlek
        movement.Start(game_map)
        admin = failsafe.set_admin
        movement_inst = movement.Movement(game_map, mapsize, admin, difficulty)
        generation.Generation(game_map, mapsize)
        movement_inst.start_move(admin)
        rto = failsafe.rto_menu()
    print("Quitting Phöz Rooms...")

if __name__ == "__main__":
    main()
