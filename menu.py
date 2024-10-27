import map
import failsafe

class Main_menu():
    
    def menu(self):
        print("-------------=+=-------------")
        print("Välkommen till The Phöz Rooms")
        choice = input("[S]tart\n[Q]uit\n: ").upper()
        print("-----------------------------")
        while True:
            if choice == "S":
                admin = failsafe.select_admin()
                print(f"DEBUGG: Admin set to: {admin}")
                diff = input("Välj din svårighetsgrad.\n[E]asy\n[N]ormal\n[H]ard\n[F]adder\n: ").upper()
                set_diff = failsafe.choice_diff(diff)  #  väljer svårighetsgrad
                print("-----------------------------")
                game_map = map.Map(set_diff, admin)  #  skapar en instans av Map
                game_map.generate_map(admin)  #  genererar spelbanan
                failsafe.retrieve_instance(game_map)
                return game_map.map, game_map.mapsize  #  retunera spelbanan och banstorlek
            elif choice == "Q":
                exit()
                return
            else:
                choice = input("Invalid choice, try again: ").upper()
