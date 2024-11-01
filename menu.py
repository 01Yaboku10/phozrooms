"""Modul för menyn till Phöz Rooms"""

import map
import failsafe

class Main_menu():
    """Klass för huvudmenyn"""
    def menu(self) -> tuple[list[list[str], int]]:
        """Huvudmenyn. Låter användern välja om de vill köra
        programmet som admin och sedan välja svårighetsgrad.
        
            Retunerar:
                game_map.map(list): spelkartan
                game_map.mapsize(int): spelkartans storlek"""
        print("-------------=+=-------------")
        print("Välkommen till The Phöz Rooms")
        choice = input("[S]tart\n[Q]uit\n: ").upper()
        while True:
            if choice == "S":
                print("-----------------------------")
                admin = failsafe.select_admin()
                print(f"DEBUGG: Admin set to: {admin}")
                diff = input("Välj din svårighetsgrad.\n[E]asy\n[N]ormal\n[H]ard\n[F]adder\n: ").upper()
                set_diff, difficulty = failsafe.choice_diff(diff)  #  väljer svårighetsgrad
                print("-----------------------------")
                game_map = map.Map(set_diff, admin)  #  skapar en instans av Map
                game_map.generate_map(admin)  #  genererar spelbanan
                failsafe.retrieve_instance(game_map)
                return game_map.map, game_map.mapsize, difficulty  #  retunera spelbanan och banstorlek
            elif choice == "Q":
                exit()
            else:
                choice = input("Invalid choice, try again: ").upper()
