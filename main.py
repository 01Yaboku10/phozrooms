import menu
import movement
import generation
import failsafe

def main():
    rto = True
    while rto:
        main_menu = menu.Main_menu()
        game_map, mapsize = main_menu.menu()  #  kör menyn och retunerar spelbanan och dess storlek
        movement.Start(game_map)
        admin = failsafe.set_admin
        movement_inst = movement.Movement(game_map, mapsize, admin)
        generation.Generation(game_map, mapsize, movement_inst)
        movement_inst.start_move()
        rto = failsafe.rto_menu()
    print("Quitting Phöz Rooms...")

main()