import colorama
from colorama import Fore, Style
import difficulty
from map import Exam, Drunkard, Phoz, Treasure
import weapon

colorama.init(autoreset=True)

def set_diff(diff):
    if diff == "E":
        set_difficulty = difficulty.easy
    elif diff == "N":
        set_difficulty = difficulty.normal
    elif diff == "H":
        set_difficulty = difficulty.hard
    else:
        set_difficulty = difficulty.fadder
    return set_difficulty

def is_spawn_limit(mapsize: int, start: int, phoz: int, exam: int, treasure: int, drunkard: int) -> bool:
    if mapsize**2 <= start + phoz + round(exam * 0.01 * mapsize**2) + treasure + round(drunkard * 0.01 * mapsize**2):
        return False
    else:
        return True
    
def slot_is_empty(game_map: list[list[str]], rand_x: int, rand_y: int, mode: str = "D", movement_inst: object = None) -> bool:
    if mode == "D":
        if game_map[rand_x][rand_y] == 0:
            return True
        else:
            return False
    elif mode == "P" and movement_inst is not None:
        if game_map[rand_x][rand_y] == 0 and movement_inst.current_row != rand_x and movement_inst.current_col != rand_y:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} rand_y: {rand_y}, current_row: {movement_inst.current_row}")
            return True
        else:
            return False
    
def is_render(row: int, col: int, mapsize: int, item: str = "0") -> str:
    left = col > 0
    right = col < mapsize - 1
    top = row > 0

    print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Render is {item}")

    if item == "E":
        return "20"
    
    renders = {
        (True, True, True): {"0": "1", "T": "7", "D": "14"},
        (True, True, False): {"0": "4", "T": "10", "D": "17"},
        (True, False, True): {"0": "5", "T": "11", "D": "18"},
        (True, False, False): {"0": "6", "T": "12", "D": "19"},
        (False, True, True): {"0": "2", "T": "8", "D": "15"},
        (False, True, False): {"0": "3", "T": "9", "D": "16"}
    }

    return renders.get((left, right, top), {}).get(item, None) # DO NOT REMOVE {}
def is_inbounce(row: int, col: int, mapsize: int) -> tuple[bool, bool, bool, bool]:
    west_isb = col > 0
    east_isb = col < mapsize -1
    south_isb = row < mapsize -1
    north_isb = row > 0
    return west_isb, east_isb, north_isb, south_isb

def is_item(get_admin: object, game_map: list[list[str]], row: int, col: int, mapsize: int, gui: object, movement_inst: object, game_map_inst: object, phoz: object):
    if get_admin.is_admin:
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Running is_item")
    items = ["E", "D", "P", "T"]
    item_dict = {
        "E": Exam("E", 1, game_map, mapsize, get_admin),
        "D": Drunkard("D", 1, game_map, mapsize, get_admin),
        "P": Phoz("P", 1, game_map, mapsize, get_admin),
        "T": Treasure("T", 1, game_map, mapsize, get_admin)
    }
    if game_map[row][col] in items:
        item = game_map[row][col]
        if get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Item found! Item: {item}")
        call_item = getattr(item_dict[item], f"init_{item.lower()}")
        if get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Calling: {item}!")
        if item == "P":
            call_item(gui, movement_inst, game_map_inst)
        else:
            call_item(gui, movement_inst)
    else:
        if get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} No item in this room.")
        if phoz.is_alive():
            if phoz.is_near(movement_inst.current_row, movement_inst.current_col):
                gui.set_message("Du kan höra gtymtningar och rosslingar...", 300)
                print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Shots taken: {phoz.shots_taken}")
                if phoz.shots_taken < 6:
                    weapon_inst = weapon.Heineken(movement_inst.current_row, movement_inst.current_col, gui, mapsize, phoz)
                    phoz.shots_taken += 1
                    gui.phoz_near(weapon_inst, weapon_inst.shots)
                else:
                    gui.set_message("Du har inga flaskor kvar...", 0.75)
            else:
                gui.ask_directions()
        
