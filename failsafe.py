import difficulty
from generation import Hole, Bats, Phoz, Treasure
import map

def select_admin():
    admin = input("Would you like to run the game as admin? [Y]/[N]: ").upper()
    while True:
        if admin == "Y":
            return is_admin("Y")
        elif admin == "N":
            return is_admin("N")
        else:
            admin = input("Invalid option, try again: ").upper()

def is_admin(isadmin):
    global set_admin
    if isadmin == "Y":
        set_admin = True
    else:
        set_admin = False
    isadmin = set_admin
    return isadmin

def map_is_empty(map, rand_x, rand_y):
    if map[rand_x][rand_y] == 0:
        return True
    else:
        return False
    
def is_spawn_limit(MAPSIZE, START, PHOZ, HOLE, TREASURE, BATS):
    if MAPSIZE**2 <= START + PHOZ + round(HOLE * 0.01 * MAPSIZE**2) + TREASURE + round(BATS * 0.01 * MAPSIZE**2):
        return False
    else:
        return True
    
def is_inbounce(current_col, current_row, mapsize):
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

def is_phoz(current_row, current_col, game_map, admin):
    if admin:
        print("DEBUGG: Running is_phoz")
    for row_i, slot in enumerate(game_map):
        if "P" in slot:
            col_i = slot.index("P")
            if admin:
                print(f"DEBUGG: Phöz is in {row_i, col_i}")
                print(f"DEBUGG: checked {abs(current_row - row_i)}, {abs(current_col - col_i)}")
            if 0 <= abs(current_row - row_i) < 2 and 0 <= abs(current_col - col_i) < 2:
                print("Du kan höra gtymtningar och rosslingar...")

def is_valid_direction(west_isb, east_isb, north_isb, south_isb, admin):
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
def retrieve_instance(game_map):
    global instance
    instance = game_map

def is_item(movement_inst, map, new_row, new_col, mapsize):
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
            call_item(map, mapsize, new_row, new_col, set_admin)
        else:
            if set_admin:
                print("DEBUGG: Calling item which is not B or T")
            call_item()
    else:
        print("No items in this room!")
        movement_inst.ask_direction()
        
def choice_diff(diff):
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
    return set_diff

def rto_menu():
    print("-----------------------------")
    choice = input("Return to menu or quit? [R]/[Q]: ").upper()
    while True:
        if choice == "R":
            return True
        elif choice == "Q":
            return False
        else:
            choice = input("Invalid choice, try again: ").upper()
