"""Felhanterings modul för Phöz Rooms"""

import difficulty
from generation import Hole, Bats, Phoz, Treasure
import phoz

def select_admin() -> bool:
    """Låter användaren välja om de vill köra programmet som Admin eller ej.
        Argument:
            admin(str): Valet användaren gör.
        
        Retunerar:
            set_admin(bool): True / False"""
    admin = input("Would you like to run the game as admin? [Y]/[N]: ").upper()
    while True:
        if admin == "Y":
            return is_admin("Y")
        elif admin == "N":
            return is_admin("N")
        else:
            admin = input("Invalid option, try again: ").upper()

def is_admin(choice: str) -> bool:
    """Används tillsammans med select_admin för att välja om programmet körs
    som admin eller inte.
        Argument:
            choice(str): Valet från select_admin
        Retunerar:
            set_admin(bool): True / False"""
    global set_admin
    if choice == "Y":
        set_admin = True
    else:
        set_admin = False
    return set_admin

def map_is_empty(map: list, rand_x: int, rand_y: int) -> bool:
    """Kollar om ett rum på kartan är tomm eller ej.
        Argument:
            map(list): Spelkartan
            rand_x(int): Ett slumpmässigt tal eller heltal
            rand_y(int): Ett slumpmässigt tal eller heltal
        Retunerar:
            True / False"""
    if map[rand_x][rand_y] == 0:
        return True
    else:
        return False
    
def is_spawn_limit(mapsize: int, start: int, phoz: int, hole: int, treasure: int, bats: int) -> bool:
    """Kollar om mängden kartobjekt överstiger storleken på kartan.
        Argument:
            mapsize(int): Storleken på kartan
            start(int): Mängden "startpoints"
            phoz(int): Mängden phöz
            hole(int): Mängden hål
            treasure(int): Mängden skatt
            bats(int): Mängden fladdermöss
        Retunerar
            True / False"""
    if mapsize**2 <= start + phoz + round(hole * 0.01 * mapsize**2) + treasure + round(bats * 0.01 * mapsize**2):
        return False
    else:
        return True
    
def is_inbounce(current_col: int, current_row: int, mapsize: int) -> tuple[bool, bool, bool, bool]:
    """Kollar vilka håll spelaren kan röra sig till.
    
        Argument:
            current_col(int): nuvarande X position
            current_row(int): nuvarande Y position
            mapsize(int): storleken på spelplanen
            
        Retunerar:
            west_isb(Bool): Ok att gå väst
            east_isb(Bool): Ok att gå öst
            south_isb(Bool): Ok att gå söder
            north_isb(Bool): Ok att gå norr"""
    west_isb = current_col > 0
    east_isb = current_col < mapsize -1
    south_isb = current_row < mapsize -1
    north_isb = current_row > 0
    return west_isb, east_isb, north_isb, south_isb

def is_valid_direction(west_isb: bool, east_isb: bool, north_isb: bool, south_isb: bool, admin: bool) -> str:
    """Frågar vart spelaren vill röra sig åt och kollar om det är innanför spelbanan.
        Argument:
            west_isb(Bool): Ok att gå väst
            east_isb(Bool): Ok att gå öst
            south_isb(Bool): Ok att gå söder
            north_isb(Bool): Ok att gå norr
        Retunerar:
            goto(str): Ett val som är ok."""
    global instance
    goto = input("Move to: ").upper()
    while True:
        if goto == "W" and west_isb \
        or goto == "E" and east_isb \
        or goto == "S" and south_isb \
        or goto == "N" and north_isb:
            return goto
        elif goto == "Q":
            print("Quitting Phöz Rooms...")
            exit()
        elif goto == "M" and admin:
            print("-----------------------------")
            print("DEBUGG: Reprinting map")
            instance.generate_map(admin)
            print("-----------------------------")
            return goto
        else:
            goto = input("Cannot move in that direction! \nTry again: ").upper()

def retrieve_instance(game_map) -> None:
    """Hämtar spelkarts instansen för att lättare använda den inom modulen"""
    global instance
    instance = game_map

def is_item(movement_inst, map: list, new_row: int, new_col: int, mapsize: int, admin: bool, diff: str) -> None:
    """Kollar om spelaren har gått till ett kartobjekt, och kallar isåfall på
    objektets funktion.
        Argument:
            movement_inst(instance): Instansen för movement klassen
            map(list): Spelkartan
            new_row(int): Den nya raden som spelaren vill gå till
            new_col(int): Den nya kolumnen som spelaren vill gå till
            mapsize(int): Kartstorleken
            admin(bool): Spelaren är admin eller ej
        Retunerar:
            None"""
    if set_admin:
        print("DEBUGG: Running is_item")
    items = ("H", "B", "P", "T")
    item_dict = {
        "H": Hole("H", 1),
        "B": Bats("B", 1),
        "P": Phoz("P", 1),
        "T": Treasure("T", 1)
    }
    if map[new_row][new_col] in items:
        item = map[new_row][new_col]
        if set_admin:
            print(f"DEBUGG: item found! Item: {item}")
        call_item = getattr(item_dict[item], f"init_{item.lower()}")
          #  hämtar namnet på objektet och kallar dess funktion
          #  Inlärt på geeksforgeeks.org
        if item in ("B", "T", "P"):
            if set_admin:
                print(f"DEBUGG: Calling {item}!")
            call_item(map, mapsize, new_row, new_col, set_admin, diff)
        else:
            if set_admin:
                print("DEBUGG: Calling item which is not B or T")
            call_item()
    else:
        print("No items in this room!")
        phoz.is_phoz(new_row, new_col, map, admin, mapsize, movement_inst)
        phoz_status = phoz.is_phoz_dead(map)
        if phoz_status:
            phoz.game_over(diff)
            return
        else:
            movement_inst.ask_direction()
        
def choice_diff(diff: str) -> tuple:
    """Sätter svårighetsgraden
        Argument:
            diff(str): Valet som spelaren valt
        
        Retunerar:
            set_diff(tuple): En tuple med attribut för respektive svårighetsgrad"""
    while True:
        if diff == "E":
            set_diff = difficulty.easy
            break
        elif diff == "N":
            set_diff = difficulty.normal
            break
        elif diff == "H":
            set_diff = difficulty.hard
            break
        elif diff == "F":
            set_diff = difficulty.fadder
            break
        else:
            diff = input("Invalid choice, try again: ").upper()
    return set_diff, diff

def rto_menu() -> bool:
    """Frågar om spelaren vill gå tillbaka till menyn eller
    avsluta programmet.
        Argument:
            choice(str): Valet spelar valt
        
        Retunerar:
            True / False"""
    print("-----------------------------")
    choice = input("Return to menu or quit? [R]/[Q]: ").upper()
    while True:
        if choice == "R":
            return True
        elif choice == "Q":
            return False
        else:
            choice = input("Invalid choice, try again: ").upper()
